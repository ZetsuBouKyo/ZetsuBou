import redis.asyncio as _async_redis
from redis.asyncio import Redis

from back.settings import setting

REDIS_URL = setting.redis_url

if REDIS_URL is not None:
    async_redis = _async_redis.from_url(REDIS_URL)
else:
    async_redis = None


async def list_pairs(key="*", async_redis: Redis = async_redis):
    async for key in async_redis.scan_iter(key):
        value = await async_redis.get(key)
        yield key, value
