from logging import Logger

import pytest

from back.init.check import ping_elasticsearch


class ElasticsearchSession:
    async def __aenter__(self):
        ping = await ping_elasticsearch()
        if not ping:
            pytest.exit("Skip because we can't connect to Elasticsearch.", returncode=0)

    async def __aexit__(self, exc_type, exc, tb):
        await self.exit()


@pytest.mark.asyncio
async def test(logger: Logger):
    async with ElasticsearchSession():
        ...
