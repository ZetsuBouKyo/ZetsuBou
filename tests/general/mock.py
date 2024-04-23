from typing import Optional
from unittest.mock import Mock

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession


def get_mock_result(first: Optional[dict] = None) -> Mock:
    result = Mock(spec=Result)
    if first is None:
        result.scalars.return_value.first.return_value = first
    else:
        result.scalars.return_value.first.return_value.__dict__ = first

    return result


def get_mock_sqlalchemy_async_session(mock_result: Mock = get_mock_result()):
    session = Mock(spec=AsyncSession)
    session.execute.return_value = mock_result
    return session


class MockAsyncIter:
    def __init__(self, items):
        self.items = items

    async def __aiter__(self):
        for item in self.items:
            yield item


class MockAsyncDatabaseSession:
    def begin(self):
        return self

    async def execute(self, *arg, **kwargs):
        pass

    def __call__(self):
        return self

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass
