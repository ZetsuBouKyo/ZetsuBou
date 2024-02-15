from pathlib import Path

from back.init.check import ping
from back.settings import setting
from tests.general.exceptions import NotFoundException

STORAGE_S3_VOLUME = setting.storage_s3_volume


class BaseIntegrationSession:
    async def check(self):
        # we use the services defined in `settings.env`
        p = await ping()
        if not p:
            raise NotFoundException("Services not found.")

        storage_s3_volume_path = Path(STORAGE_S3_VOLUME)
        if not storage_s3_volume_path.exists():
            raise NotFoundException(f"`{storage_s3_volume_path}` not found.")

    async def __aenter__(self):  # pragma: no cover
        await self.check()
        await self.enter()

    async def __aexit__(self, exc_type, exc, tb):  # pragma: no cover
        await self.exit()

    async def enter(self):
        ...

    async def exit(self):
        ...
