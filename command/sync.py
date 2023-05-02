import time

import typer
from back.crud.gallery import CrudSyncGalleryMinioStorage
from back.crud.video import CrudSyncVideoMinioStorage
from back.db.crud import CrudMinioStorage
from back.db.model import MinioStorageCategoryEnum

from command.router import register
from command.utils import sync

_help = """
Synchronize the information of Gallery and Video from Minio storages.

* Gallery:

The synchronization would be based on the `[gallery]/.tag/gallery.json` if it exists.

* Video:

The synchronization would be based on video file (file name, first frame of video, and so on).
"""  # noqa
app = typer.Typer(name="sync", help=_help)


@app.command()
@sync
@register("sync-minio-storage", "sync sync-minio-storage")
async def sync_minio_storage(
    id: int = typer.Argument(..., help="The id of the minio storage.")
):
    """
    Synchronize specific minio storages by id.
    """

    print(f"Minio storage id: {id}")
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
@register("sync-gallery-minio-storages", "sync sync-gallery-minio-storages")
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
@register("sync-minio-storages", "sync sync-minio-storages")
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
