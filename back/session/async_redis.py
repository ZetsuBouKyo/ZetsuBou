import logging
from uuid import uuid4

import redis.asyncio as _async_redis
from back.logging import logger_webapp
from back.settings import setting
from redis.asyncio import Redis

REDIS_URL = setting.redis_url

async_redis = _async_redis = _async_redis.from_url(REDIS_URL)


async def list_pairs(key="*", async_redis: Redis = async_redis):
    async for key in async_redis.scan_iter(key):
        value = await async_redis.get(key)
        yield key, value


def get_progress_id(prefix: str = ""):
    id_body = str(uuid4())
    if prefix:
        return f"{prefix}.{id_body}"
    return id_body


class Progress:
    def __init__(
        self,
        iterable,
        id: str = None,
        initial: int = 0,
        final: int = 100,
        total: int = None,
        async_redis: Redis = None,
        is_from_setting_if_none: bool = False,
    ):
        if id is None:
            self.id = get_progress_id()
        else:
            self.id = id

        self.initial = self._initial = initial
        self.final = final
        self._interval = self.final - self.initial

        if total is None:
            self.total = len(iterable)
        else:
            self.total = total

        if logger_webapp.level == logging.DEBUG:
            self._last_progress = int(self._initial)

        self.async_redis = async_redis
        self._iterable = iterable

        if is_from_setting_if_none:
            if async_redis is None:
                self.async_redis = _async_redis

    async def _set(self, progress: float):
        _progress = f"{progress:.2f}"
        await self.async_redis.set(self.id, _progress)

    async def _update(self):
        self._initial += 1 / self.total * self._interval

        if logger_webapp.level == logging.DEBUG:
            self._current_progress = int(self._initial)
            if self._current_progress != self._last_progress:
                self._last_progress = self._current_progress
                if self._current_progress % 10 == 0:
                    logger_webapp.debug(f"progress: {self._current_progress} %")

        await self._set(self._initial)

    async def __aiter__(self):
        if hasattr(self._iterable, "__aiter__"):
            async for obj in self._iterable:
                await self._update()
                yield obj
        else:
            for obj in self._iterable:
                await self._update()
                yield obj

        await self._set(self.final)
