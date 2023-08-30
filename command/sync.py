import time

import typer
from elasticsearch import AsyncElasticsearch

from back.crud.async_sync import get_crud_sync
from back.db.crud import CrudStorageMinio
from back.init.async_elasticsearch import create_gallery
from back.model.base import SourceProtocolEnum
from back.model.task import ZetsuBouTaskProgressEnum
from back.settings import setting
from lib.typer import ZetsuBouTyper

_help = """
Synchronize the information of Gallery and Video from Minio storages.

* Gallery:
The synchronization would be based on the `[gallery]/.tag/gallery.json` if it exists.

* Video:
The synchronization would be based on video file (file name, first frame of video, and
so on).
"""  # noqa
app = ZetsuBouTyper(name="sync", help=_help)

ELASTICSEARCH_URLS = setting.elastic_urls


@app.command(
    name="storage",
    airflow_dag_id="sync-storage",
    airflow_dag_sub_command="sync storage",
)
async def _storage(
    protocol: SourceProtocolEnum = typer.Argument(..., help="Storage protocol."),
    storage_id: int = typer.Argument(..., help="Storage ID."),
    progress: bool = typer.Option(
        default=True, help="Send progress information to Redis."
    ),
    elasticsearch_urls: str = typer.Option(
        default=ELASTICSEARCH_URLS, help="Elasticsearch URLs separated by `,`."
    ),
    target_index: str = typer.Option(default=None, help="Target Elasticsearch index."),
):
    """
    Synchronize the storage with protocol and storage ID.
    """

    # create `target_index` if it is not None and does not exist
    elasticsearch_hosts = elasticsearch_urls.split(",")
    async_elasticsearch = AsyncElasticsearch(hosts=elasticsearch_hosts)
    if target_index is not None:
        await create_gallery(async_elasticsearch, target_index)

    ti = time.time()

    crud = await get_crud_sync(
        protocol, storage_id, is_progress=progress, target_index=target_index
    )
    await crud.sync()

    tf = time.time()
    td = tf - ti
    print(f"total time: {td}(s)")


@app.command(
    name="storages",
    airflow_dag_id="sync-storages",
    airflow_dag_sub_command="sync storages",
)
async def _storages(
    progress: bool = typer.Option(
        True, "-p/", "--progress/", help="Send progress information to Redis."
    ),
):
    """
    Synchronize all storages.
    """

    skip = 0
    limit = 100
    t = 0

    protocol = SourceProtocolEnum.MINIO.value
    all_minio_storages = []

    minio_storages = await CrudStorageMinio.get_rows_order_by_id(skip=skip, limit=limit)
    all_minio_storages += minio_storages

    while len(minio_storages) > 0:
        skip += limit
        minio_storages = await CrudStorageMinio.get_rows_order_by_id(
            skip=skip, limit=limit
        )
        all_minio_storages += minio_storages

    progress_id = ZetsuBouTaskProgressEnum.SYNC_STORAGES
    total_storages = len(all_minio_storages)
    total_storages_0 = total_storages - 1
    interval = 100 / total_storages
    initial = 0.0
    final = initial + interval

    for i, minio_storage in enumerate(all_minio_storages):
        ti = time.time()

        crud = await get_crud_sync(
            protocol,
            minio_storage.id,
            progress_id=progress_id,
            progress_initial=initial,
            progress_final=final,
            is_progress=progress,
        )
        await crud.sync()

        if i == total_storages_0:
            initial, final = final, 100.0
        else:
            initial = final
            final += interval

        tf = time.time()
        td = tf - ti
        t += td
        print(f"Protocol: {protocol} Storage ID: {minio_storage.id} Time: {td}")

    print(f"total time: {t}(s)")
