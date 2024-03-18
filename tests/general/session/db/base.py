import os

from sqlalchemy import event
from sqlalchemy.engine import Engine

from back.init.check import ping_postgres
from back.init.database import init_table
from back.session.async_db import async_session
from back.settings import setting
from tests.general.logger import logger

DATABASE_URL_SQLITE = setting.test_database_url_sqlite
DATABASE_URL_POSTGRESQL = setting.test_database_url_postgresql
TEST_VOLUMES_TESTS_DATABASE_SQLITE = setting.test_volumes_database_sqlite


class DatabaseSession:
    async def __aenter__(self):
        await self.init()
        await self.enter()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.exit()

    async def init(self):  # pragma: no cover
        is_postgres = await ping_postgres(database_url=DATABASE_URL_POSTGRESQL)
        if is_postgres:
            logger.info("Initializing PostgreSQL...")
            database_url = DATABASE_URL_POSTGRESQL
        else:
            logger.info("Initializing SQLite...")
            database_url = DATABASE_URL_SQLITE
            os.makedirs(TEST_VOLUMES_TESTS_DATABASE_SQLITE, exist_ok=True)

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, _):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        async_session.load(database_url)
        self.async_session = async_session

        await init_table()

    async def enter(self): ...

    async def exit(self): ...
