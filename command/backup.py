import io
import json
from pathlib import Path
from typing import List, Union

from back.crud.elastic import CrudElasticBase
from back.db.crud.base import (
    flatten_dependent_tables,
    get_dependent_tables,
    get_primary_key_names_by_table_instance,
    get_rows_order_by,
    get_table_instances,
    list_tables,
    reset_auto_increment,
)
from back.session.async_db import async_session
from back.session.elastic import elastic_client, indices, init_index
from back.session.init_db import create_tables
from back.session.minio import minio_client
from back.settings import setting
from back.utils.dt import get_now
from elasticsearch import helpers
from elasticsearch.exceptions import RequestError
from minio.error import S3Error
from sqlalchemy.orm.decl_api import DeclarativeMeta
from tqdm import tqdm

from command.router import register
from command.utils import sync

backup_bucket_name = setting.minio_backup_bucket_name
db_object_name = "db"
elastic_object_name = "elastic"


# TODO:
async def get_all_rows(instance: DeclarativeMeta) -> List[dict]:
    out = []
    skip = 0
    limit = 1000
    rows = await get_rows_order_by(instance, instance.id, skip=skip, limit=limit)
    while rows:
        out += rows
        skip += limit
        rows = await get_rows_order_by(instance, instance.id, skip=skip, limit=limit)

    return out


async def loads_from_json_with_instance(instance: DeclarativeMeta, rows: List[dict]):
    async with async_session() as session:
        async with session.begin():
            for row in rows:
                row = instance(**row)
                session.add(row)


async def loads_from_json_file(fpath: Union[str, Path]):
    if type(fpath) is str:
        fpath = Path(fpath)
    if not fpath.exists():
        print(f"{fpath} not found")
        return

    table_instances = get_table_instances()
    table_name = fpath.stem
    table_instance = table_instances.get(table_name, None)
    if table_instance is None:
        print(f"table: {table_name} not found")
        return

    with fpath.open(mode="r", encoding="utf-8") as fp:
        rows = json.load(fp)

    await loads_from_json_with_instance(table_instance, rows)


class Backup:
    """Backup the databases in ZetsuBou."""

    @sync
    @register("backup-dump", "backup dump")
    async def dump(self, encoding: str = "utf-8"):
        root_object_name = get_now().replace(":", "-").replace(".", "-")

        table_names = list_tables()
        table_instances = get_table_instances()

        for table_name in tqdm(table_names):
            table_class = table_instances[table_name]
            rows = await get_all_rows(table_class)
            rows = json.dumps(rows).encode(encoding=encoding)

            data = io.BytesIO(rows)
            object_name = "/".join(
                [root_object_name, db_object_name, f"{table_name}.json"]
            )
            minio_client.put_object(
                backup_bucket_name,
                object_name,
                data,
                len(data.getvalue()),
                content_type="application/json",
            )

        for index in tqdm(indices):
            print(f"index: {index}")
            if index == setting.elastic_index_tag:
                sorting = ["_score", {"id": "asc"}]
            else:
                sorting = ["_score", {"id.keyword": "asc"}]
            crud = CrudElasticBase(index=index, size=1000, sorting=sorting)
            page = 1
            try:
                results = crud.match(page, "")
            except RequestError:
                continue
            rows = []
            while results.hits.hits:
                for hit in results.hits.hits:
                    source = hit.source
                    if type(source) is dict:
                        rows.append(source)
                    else:
                        rows.append(source.dict())
                page += 1
                results = crud.match_all(page)

            rows = json.dumps(rows).encode(encoding=encoding)

            data = io.BytesIO(rows)
            object_name = "/".join(
                [root_object_name, elastic_object_name, f"{index}.json"]
            )
            minio_client.put_object(
                backup_bucket_name,
                object_name,
                data,
                len(data.getvalue()),
                content_type="application/json",
            )

    @sync
    @register("backup-load", "backup load")
    async def load(self, date: str):
        await create_tables()

        table_instances = get_table_instances()
        table_dependents = {
            table_name: get_dependent_tables(table_instance)
            for table_name, table_instance in table_instances.items()
        }
        table_names = flatten_dependent_tables(table_dependents)

        for table_name in tqdm(table_names):
            object_name = "/".join([date, db_object_name, f"{table_name}.json"])
            rows = minio_client.get_object(backup_bucket_name, object_name)
            rows = json.load(rows)

            table_instance = table_instances.get(table_name, None)
            if table_instance is None:
                print(f"table: {table_name} not found")
                return

            await loads_from_json_with_instance(table_instance, rows)
            pk_names = get_primary_key_names_by_table_instance(table_instance)
            for pk_name in pk_names:
                seq = f"{table_name}_{pk_name}_seq"
                await reset_auto_increment(table_name, seq=seq)

        init_index()
        size = 1000
        for index in tqdm(indices):
            object_name = "/".join([date, elastic_object_name, f"{index}.json"])
            try:
                rows = minio_client.get_object(backup_bucket_name, object_name)
            except S3Error:
                continue

            rows = json.load(rows)

            i = 0
            batch = rows[i * size : (i + 1) * size]
            while batch:
                actions = [
                    {"_index": index, "_id": source["id"], "_source": source}
                    for source in batch
                ]
                helpers.bulk(elastic_client, actions)
                i += 1
                batch = rows[i * size : (i + 1) * size]
