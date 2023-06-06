import pytest
from back.init.async_elasticsearch import init_indices
from back.init.database import init_table


@pytest.mark.asyncio
async def test_init():
    await init_indices()
    await init_table()
