import io
import json
from pathlib import Path
from typing import List, Union

import typer
from elasticsearch.helpers import async_bulk, async_scan
from sqlalchemy.orm.decl_api import DeclarativeMeta
from tqdm import tqdm

from back.db.crud.base import (
    flatten_dependent_tables,
    get_all_rows_order_by_id,
    get_primary_key_names_by_table_instance,
    get_table_instances,
    list_tables,
    reset_auto_increment,
)
from back.init.async_elasticsearch import indices, init_indices
from back.init.database import create_tables
from back.model.base import SourceBaseModel
from back.session.async_db import async_session
from back.session.async_elasticsearch import get_async_elasticsearch
from back.session.storage import get_app_storage_session
from back.settings import setting
from back.utils.dt import get_now
from lib.typer import ZetsuBouTyper

STORAGE_BACKUP = setting.storage_backup

BACKUP_DATABASE = "db"
BACKUP_ELASTICSEARCH = "elastic"

STORAGE_PROTOCOL = setting.storage_protocol
STORAGE_BACKUP = setting.storage_backup


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


def get_database_table_source(backup_date: str, table_name: str):
    data_path = f"{STORAGE_PROTOCOL}://{STORAGE_BACKUP}/{backup_date}/{BACKUP_DATABASE}/{table_name}.json"  # noqa
    return SourceBaseModel(path=data_path)


def get_elasticsearch_index_source(backup_date: str, index: str):
    data_path = f"{STORAGE_PROTOCOL}://{STORAGE_BACKUP}/{backup_date}/{BACKUP_ELASTICSEARCH}/{index}.json"  # noqa
    return SourceBaseModel(path=data_path)


def get_body(data: dict, encoding: str = "utf-8"):
    json_str = json.dumps(data).encode(encoding=encoding)
    return io.BytesIO(json_str)


async def _load_table(table_name: str, table_instance, rows: List[dict]):
    if table_instance is None:
        print(f"table: {table_name} not found")
        return

    await loads_from_json_with_instance(table_instance, rows)
    pk_names = get_primary_key_names_by_table_instance(table_instance)
    for pk_name in pk_names:
        seq = f"{table_name}_{pk_name}_seq"
        await reset_auto_increment(table_name, seq=seq)


_help = """
Backup the databases.

Export the SQL databases and Elasticsearch indices into minio repository in the form of
 JSON.
"""

app = ZetsuBouTyper(name="backup", help=_help)


@app.command(airflow_dag_id="backup-dump", airflow_dag_sub_command="backup dump")
async def dump(
    encoding: str = typer.Option(
        default="utf-8", help="The encoding of the output JSON files."
    )
):
    """
    Dump the SQL databases and elasticsearch indices into JSON in minio.
    """
    async_elasticsearch = get_async_elasticsearch()

    backup_date = get_now().replace(":", "-").replace(".", "-")

    table_names = list_tables()
    table_instances = get_table_instances()

    storage_session = get_app_storage_session(is_from_setting_if_none=True)
    async with storage_session:
        for table_name in tqdm(table_names):
            table_class = table_instances[table_name]
            rows = await get_all_rows_order_by_id(table_class)

            body = get_body(rows, encoding=encoding)
            table_source = get_database_table_source(backup_date, table_name)

            await storage_session.put_object(
                table_source, body, content_type="application/json"
            )

        for index in tqdm(indices):
            print(f"index: {index}")

            rows = []
            query = {"query": {"match_all": {}}}
            async for doc in async_scan(
                client=async_elasticsearch, query=query, index=index
            ):
                source = doc.get("_source", None)
                if source is None:
                    continue
                rows.append(source)

            body = get_body(rows, encoding=encoding)
            index_source = get_elasticsearch_index_source(backup_date, index)

            await storage_session.put_object(
                index_source, body, content_type="application/json"
            )
    await async_elasticsearch.close()


@app.command(airflow_dag_id="backup-load", airflow_dag_sub_command="backup load")
async def load(
    date: str = typer.Argument(
        ...,
        help="The dumping date which could be found under the path [root-to-minio-data]/backup .",  # noqa
    )
):
    """
    Load the SQL databases and elasticsearch indices from JSON in minio. Be careful, We
    must run this command before running the ZetsuBou webapp.
    """
    async_elasticsearch = get_async_elasticsearch()

    await create_tables()

    table_instances = get_table_instances()
    table_names = flatten_dependent_tables()

    storage_session = get_app_storage_session(is_from_setting_if_none=True)
    async with storage_session:
        for table_name in tqdm(table_names):
            table_source = get_database_table_source(date, table_name)
            rows = await storage_session.get_json(table_source)
            if rows is None:
                continue
            table_instance = table_instances.get(table_name, None)

            await _load_table(table_name, table_instance, rows)

        await init_indices()
        size = 1000
        for index in tqdm(indices):
            index_source = get_elasticsearch_index_source(date, index)
            rows = await storage_session.get_json(index_source)

            i = 0
            batch = rows[i * size : (i + 1) * size]
            while batch:
                actions = [
                    {"_index": index, "_id": source["id"], "_source": source}
                    for source in batch
                ]
                await async_bulk(async_elasticsearch, actions)

                i += 1
                batch = rows[i * size : (i + 1) * size]


@app.command(airflow_dag_id="backup-load", airflow_dag_sub_command="backup load")
async def load_table(
    table: str = typer.Argument(..., help="Table JSON path."),
    table_name: str = typer.Option(default=None, help="Table JSON path."),
):
    """
    Load data from JSON into an SQL table.
    """
    table_path = Path(table)
    if table_name is None:
        table_name = table_path.stem

    with table_path.open(mode="r") as fp:
        rows = json.load(fp)

    table_instances = get_table_instances()
    table_instance = table_instances.get(table_name, None)

    await _load_table(table_name, table_instance, rows)
