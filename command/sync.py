import time

import typer
from back.crud.async_sync import get_crud_sync
from back.crud.gallery import CrudSyncGalleryStorageMinio
from back.crud.video import CrudSyncVideoStorageMinio
from back.db.crud import CrudStorageMinio
from back.model.base import SourceProtocolEnum
from back.model.storage import StorageCategoryEnum

from command.utils import airflow_dag_register, sync

_help = """
Synchronize the information of Gallery and Video from Minio storages.

* Gallery:
The synchronization would be based on the `[gallery]/.tag/gallery.json` if it exists.

* Video:
The synchronization would be based on video file (file name, first frame of video, and
so on).
"""  # noqa
app = typer.Typer(name="sync", help=_help)


@app.command()
@sync
@airflow_dag_register("sync-minio-storage", "sync sync-minio-storage")
async def sync_minio_storage(
    id: int = typer.Argument(..., help="The id of the minio storage.")
):
    """
    Synchronize specific minio storages by id.
    """

    print(f"Storage MinIO ID: {id}")
    ti = time.time()
    minio_storage = await CrudStorageMinio.get_row_by_id(id)
    if minio_storage.category == StorageCategoryEnum.gallery.value:
        crud = CrudSyncGalleryStorageMinio(minio_storage)
        crud.sync()
    elif minio_storage.category == StorageCategoryEnum.video.value:
        crud = CrudSyncVideoStorageMinio(minio_storage)
        crud.sync()
    tf = time.time()
    td = tf - ti
    print(f"total time: {td}(s)")


@app.command()
@sync
@airflow_dag_register("sync-gallery-minio-storages", "sync sync-gallery-minio-storages")
async def sync_gallery_minio_storages():
    """
    Synchronize all minio storages with Gallery type.
    """

    category = StorageCategoryEnum.gallery.value
    async for minio_storages in await CrudStorageMinio.iter_by_category_order_by_id(
        category
    ):
        for minio_storage in minio_storages:
            crud = CrudSyncGalleryStorageMinio(minio_storage)
            crud.sync()


@app.command()
@sync
@airflow_dag_register("sync-minio-storages", "sync sync-minio-storages")
async def sync_minio_storages():
    """
    Synchronize all minio storages.
    """

    skip = 0
    limit = 100
    t = 0
    minio_storages = await CrudStorageMinio.get_rows_order_by_id(skip=skip, limit=limit)
    while len(minio_storages) > 0:
        for minio_storage in minio_storages:
            ti = time.time()

            if minio_storage.category == StorageCategoryEnum.gallery.value:
                crud = CrudSyncGalleryStorageMinio(minio_storage)
                crud.sync()
            elif minio_storage.category == StorageCategoryEnum.video.value:
                crud = CrudSyncVideoStorageMinio(minio_storage)
                crud.sync()

            tf = time.time()
            td = tf - ti
            t += td
            print(td)

        skip += limit
        minio_storages = await CrudStorageMinio.get_rows_order_by_id(
            skip=skip, limit=limit
        )

    print(f"total time: {t}(s)")


@app.command(name="storage")
@sync
@airflow_dag_register("sync-storage", "sync storage")
async def _storage(
    protocol: SourceProtocolEnum = typer.Argument(..., help="Storage protocol."),
    storage_id: int = typer.Argument(..., help="Storage ID."),
):
    ti = time.time()

    crud = await get_crud_sync(protocol, storage_id)
    await crud.sync()

    tf = time.time()
    td = tf - ti
    print(f"total time: {td}(s)")


@app.command(name="storages")
@sync
@airflow_dag_register("sync-storages", "sync storages")
async def _storages():
    """
    Synchronize all storages.
    """

    skip = 0
    limit = 100
    t = 0

    protocol = SourceProtocolEnum.MINIO.value
    minio_storages = await CrudStorageMinio.get_rows_order_by_id(skip=skip, limit=limit)
    while len(minio_storages) > 0:
        for minio_storage in minio_storages:
            ti = time.time()

            crud = await get_crud_sync(protocol, minio_storage.id)
            await crud.sync()

            tf = time.time()
            td = tf - ti
            t += td
            print(f"Protocol: {protocol} Storage ID: {minio_storage.id} Time: {td}")

        skip += limit
        minio_storages = await CrudStorageMinio.get_rows_order_by_id(
            skip=skip, limit=limit
        )

    print(f"total time: {t}(s)")
