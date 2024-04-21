from pathlib import Path
from typing import List, Optional

from back.crud.async_sync import get_crud_sync
from back.db.model import StorageMinio
from back.init.check import ping
from back.model.gallery import Gallery
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from back.utils.gen.gallery import generate_simple_galleries
from lib.faker import ZetsuBouFaker
from lib.zetsubou.exceptions import NotFoundException, ServicesNotFoundException

ELASTICSEARCH_INDEX_GALLERY = setting.elastic_index_gallery

STORAGE_S3_VOLUME = setting.storage_s3_volume


class BaseIntegrationSession:
    async def check(self):
        # we use the services defined in `settings.env`
        p = await ping()
        if not p:
            raise ServicesNotFoundException

        storage_s3_volume_path = Path(STORAGE_S3_VOLUME)
        if not storage_s3_volume_path.exists():
            raise NotFoundException(f"`{storage_s3_volume_path}` not found.")

    async def __aenter__(self):  # pragma: no cover
        await self.check()
        await self.enter()
        return self

    async def __aexit__(self, exc_type, exc, tb):  # pragma: no cover
        await self.exit()

    async def enter(self):
        ...

    async def exit(self):
        ...

        ...


class SimpleGalleryIntegrationSession(BaseIntegrationSession):
    def __init__(
        self,
        faker: ZetsuBouFaker = ZetsuBouFaker(),
        gallery_dir_name: str = setting.gallery_dir_fname,
        gallery_tag_fname: str = setting.gallery_tag_fname,
        sync_force: bool = True,
        sync_is_progress: bool = False,
    ):
        self.faker = faker
        self.gallery_dir_name = gallery_dir_name
        self.gallery_tag_fname = gallery_tag_fname
        self.sync_force = sync_force
        self.sync_is_progress = sync_is_progress

        self.storage_session: Optional[AsyncS3Session] = None
        self.storage: Optional[StorageMinio] = None
        self.galleries: List[Gallery] = []

    async def enter(self):
        self.galleries = []
        self.storage, self.storage_session = await generate_simple_galleries()

        crud = await get_crud_sync(
            self.storage.source.protocol,
            self.storage.id,
            force=self.sync_force,
            is_progress=self.sync_is_progress,
        )
        await crud.sync()

        async with self.storage_session:
            async for gallery_source in self.storage_session.iter_directories(
                self.storage.source, self.storage.depth
            ):
                gallery_tag_source = gallery_source.get_joined_source(
                    self.gallery_dir_name, self.gallery_tag_fname
                )
                gallery_tag = await self.storage_session.get_json(gallery_tag_source)
                self.galleries.append(Gallery(**gallery_tag))

    async def exit(self):
        ...
