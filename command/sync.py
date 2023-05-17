import time

import typer
from back.crud.gallery import CrudSyncGalleryMinioStorage, get_crud_sync_gallery
from back.crud.video import CrudSyncVideoMinioStorage
from back.db.crud import CrudMinioStorage
from back.db.model import MinioStorageCategoryEnum
from back.model.base import Protocol

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
    minio_storage = await CrudMinioStorage.get_row_by_id(id)
    if minio_storage.category == MinioStorageCategoryEnum.gallery.value:
        crud = CrudSyncGalleryMinioStorage(minio_storage)
        crud.sync()
    elif minio_storage.category == MinioStorageCategoryEnum.video.value:
        crud = CrudSyncVideoMinioStorage(minio_storage)
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

    category = MinioStorageCategoryEnum.gallery.value
    async for minio_storages in await CrudMinioStorage.iter_by_category_order_by_id(
        category
    ):
        for minio_storage in minio_storages:
            crud = CrudSyncGalleryMinioStorage(minio_storage)
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
    minio_storages = await CrudMinioStorage.get_rows_order_by_id(skip=skip, limit=limit)
    while len(minio_storages) > 0:
        for minio_storage in minio_storages:
            if minio_storage.category == MinioStorageCategoryEnum.gallery.value:
                crud = CrudSyncGalleryMinioStorage(minio_storage)
                crud.sync()
            elif minio_storage.category == MinioStorageCategoryEnum.video.value:
                crud = CrudSyncVideoMinioStorage(minio_storage)
                crud.sync()
        skip += limit
        minio_storages = await CrudMinioStorage.get_rows_order_by_id(
            skip=skip, limit=limit
        )


@app.command(name="storage")
@sync
@airflow_dag_register("sync-storage", "sync storage")
async def _storage(
    protocol: Protocol = typer.Argument(..., help="Storage protocol."),
    storage_id: int = typer.Argument(..., help="Storage ID."),
):
    ti = time.time()

    crud = await get_crud_sync_gallery(protocol, storage_id)
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
    ti = time.time()

    skip = 0
    limit = 100

    protocol = Protocol.MINIO.value
    minio_storages = await CrudMinioStorage.get_rows_order_by_id(skip=skip, limit=limit)
    while len(minio_storages) > 0:
        for minio_storage in minio_storages:
            if minio_storage.category == MinioStorageCategoryEnum.gallery.value:
                crud = await get_crud_sync_gallery(protocol, minio_storage.id)
                await crud.sync()
            elif minio_storage.category == MinioStorageCategoryEnum.video.value:
                crud = CrudSyncVideoMinioStorage(minio_storage)
                crud.sync()
        skip += limit
        minio_storages = await CrudMinioStorage.get_rows_order_by_id(
            skip=skip, limit=limit
        )

    tf = time.time()
    td = tf - ti
    print(f"total time: {td}(s)")
