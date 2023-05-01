import time

from back.crud.gallery import CrudSyncGalleryMinioStorage
from back.crud.video import CrudSyncVideoMinioStorage
from back.db.crud import CrudMinioStorage
from back.db.model import MinioStorageCategoryEnum

from command.router import register
from command.utils import sync


class Sync:
    """Synchronize the information of Gallery and Video from Minio storages.

    - Gallery:
        The synchronization would be based on the `<gallery>/.tag/gallery.json` if it exists.
    - Video:
        The synchronization would be based on video itself.

    """

    @sync
    @register("sync-minio-storage", "sync sync_minio_storage")
    async def sync_minio_storage(self, id: int):
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

    @sync
    @register("sync-gallery-minio-storages", "sync sync_gallery_minio_storages")
    async def sync_gallery_minio_storages(self):
        """Synchronize all minio storages with Gallery type."""
        category = MinioStorageCategoryEnum.gallery.value
        async for minio_storages in await CrudMinioStorage.iter_by_category_order_by_id(
            category
        ):
            for minio_storage in minio_storages:
                crud = CrudSyncGalleryMinioStorage(minio_storage)
                crud.sync()

    @sync
    @register("sync-minio-storages", "sync sync_minio_storages")
    async def sync_minio_storages(self):
        """Synchronize all minio storages."""
        skip = 0
        limit = 100
        minio_storages = await CrudMinioStorage.get_rows_order_by_id(
            skip=skip, limit=limit
        )
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
