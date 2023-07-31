import logging
from uuid import uuid4

from redis.asyncio import Redis

from back.logging import logger_zetsubou
from back.model.task import ZetsuBouTaskProgressEnum
from back.session.async_redis import async_redis as _async_redis


def get_progress_id(prefix: str = ""):
    id_body = str(uuid4())
    if prefix:
        return f"{prefix}.{id_body}"
    return id_body


def check_airflow_progress(progress_id: str) -> bool:
    if progress_id == ZetsuBouTaskProgressEnum.SYNC_STORAGES:
        return True
    elif progress_id.startswith(ZetsuBouTaskProgressEnum.SYNC_STORAGE):
        return True
    return False


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
        if self.total == 0:
            self.total = float("inf")

        self._step = self._interval / self.total

        if logger_zetsubou.level == logging.DEBUG:
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
        self._initial += self._step

        if logger_zetsubou.level == logging.DEBUG:
            self._current_progress = int(self._initial)
            if self._current_progress != self._last_progress:
                self._last_progress = self._current_progress
                if self._current_progress % 10 == 0:
                    logger_zetsubou.debug(f"progress: {self._current_progress} %")

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
