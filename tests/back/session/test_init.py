import pytest
from back.session.elastic import init_index
from back.session.init_db import init_table
from back.session.minio import init_minio


@pytest.mark.asyncio
async def test_init():
    init_index()
    init_minio()
    await init_table()
