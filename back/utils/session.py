from functools import wraps

from lib.zetsubou.exceptions import SessionNotFoundException


class AsyncSession:
    async def open(self): ...

    async def close(self): ...

    async def __aenter__(self):
        await self.open()
        self._closed = False
        return self

    async def __aexit__(self, exc_type, exc, tb):
        self._closed = True
        await self.close()


def check_session(sess: AsyncSession):
    if not hasattr(sess, "_closed"):
        raise SessionNotFoundException
    if sess._closed:
        raise SessionNotFoundException


def session(f):
    @wraps(f)
    async def wrap(self: AsyncSession, *args, **kwargs):
        check_session(self)
        return await f(self, *args, **kwargs)

    return wrap
