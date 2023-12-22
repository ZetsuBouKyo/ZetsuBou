import pytest

from back.init.check import ping_elasticsearch
from tests.general.exceptions import NotFoundException


class ElasticsearchSession:
    async def __aenter__(self):  # pragma: no cover
        ping = await ping_elasticsearch()
        if not ping:
            raise NotFoundException("Elasticsearch not found.")

    async def __aexit__(self, exc_type, exc, tb):  # pragma: no cover
        ...


@pytest.mark.asyncio
async def test():  # pragma: no cover
    async with ElasticsearchSession():
        ...
