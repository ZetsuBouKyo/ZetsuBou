import redis.asyncio as _async_redis
from back.settings import setting
from redis.asyncio import Redis

REDIS_URL = setting.redis_url

async_redis = _async_redis.from_url(REDIS_URL)


async def list_pairs(key="*", async_redis: Redis = async_redis):
    async for key in async_redis.scan_iter(key):
        value = await async_redis.get(key)
        yield key, value
