from back.settings import setting
from lib.redis import ZetsuBouAsyncRedis

REDIS_URL = setting.redis_url


def get_async_redis_session(url: str = REDIS_URL, **kwargs) -> ZetsuBouAsyncRedis:
    if url is not None:
        return ZetsuBouAsyncRedis.from_url(url, **kwargs)
    return None


async_redis = get_async_redis_session()
