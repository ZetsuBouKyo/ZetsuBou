import asyncio

import pytest

from back.utils.session import AsyncSession, session
from lib.zetsubou.exceptions import SessionNotFoundException


def test_async_close():
    class A(AsyncSession):
        async def close(self): ...

    A()


def test_close():
    class D(AsyncSession):
        def close(self): ...

    # TODO: Should raise RuntimeError
    D()


def test_init():

    class A(AsyncSession):
        async def close(self): ...

    class B(A):
        def __init__(self, name):
            self.name = name

    name = "name"
    assert B(name).name == name


@pytest.mark.asyncio(scope="session")
async def test_session():
    class A(AsyncSession):
        async def close(self): ...

        @session
        async def add(self, x: int, y: int):
            await asyncio.sleep(1.0)
            return x + y

    async with A() as sess:
        result = await sess.add(1, 1)
        assert result == 2

    with pytest.raises(SessionNotFoundException):
        await A().add(1, 1)
