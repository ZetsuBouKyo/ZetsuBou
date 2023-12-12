from httpx import AsyncClient
from httpx._client import U


class ZetsuBouAsyncClient(AsyncClient):
    async def __aenter__(self: U) -> U:
        await self._transport.app.router.startup()
        await super().__aenter__()
        return self
