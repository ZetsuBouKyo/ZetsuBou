import logging
import os
import sys
from pathlib import Path

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from back.init.database import init_table
from back.init.logger import stream_handler
from back.session.async_db import async_session
from back.settings import setting

sys.path.append(str(Path.cwd()))

from app import app  # noqa: 402


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)


DATABASE_URL_SQLITE = setting.test_database_url_sqlite
TEST_VOLUMES_TESTS_DATABASE_SQLITE = setting.test_volumes_tests_database_sqlite


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_sqlite():
    os.makedirs(TEST_VOLUMES_TESTS_DATABASE_SQLITE, exist_ok=True)

    database_url = DATABASE_URL_SQLITE
    async_session.load(database_url)

    await init_table()


@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    logger = logging.getLogger("zetsubou.tests")
    logger.addHandler(stream_handler)
    print("\n")
    return logger
