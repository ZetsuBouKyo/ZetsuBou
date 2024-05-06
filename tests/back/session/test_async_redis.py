import pytest

from back.session.async_redis import async_redis, get_async_redis_session
from lib.faker import ZetsuBouFaker
from tests.general.logging import logger
from tests.general.session import BaseIntegrationSession


@pytest.mark.asyncio
@pytest.mark.integration
async def test_async_redis():
    async with BaseIntegrationSession():
        faker = ZetsuBouFaker()
        key = faker.random_string()
        value = faker.random_string()
        logger.info(f"key: {key}")
        logger.info(f"value: {value}")
        await async_redis.set(key, value)
        async for k, v in async_redis.list_pairs():
            k = k.decode("utf-8")
            v = v.decode("utf-8")
            if k == key and v == value:
                break
        else:
            assert False, f"pair ({key}, {value}) not found"
        await async_redis.delete(key)


def test_get_async_redis_session():
    assert get_async_redis_session(url=None) is None
