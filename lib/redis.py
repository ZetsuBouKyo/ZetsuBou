from redis.asyncio.client import Redis


class ZetsuBouAsyncRedis(Redis):
    async def list_pairs(self, key="*"):
        async for k in self.scan_iter(key):
            v = await self.get(k)
            yield k, v
