import os

from sqlalchemy import text

from back.init.database import init_table
from back.session.async_db import async_session
from back.settings import setting
from tests.general.logger import logger

DATABASE_URL_SQLITE = setting.test_database_url_sqlite
TEST_VOLUMES_TESTS_DATABASE_SQLITE = setting.test_volumes_database_sqlite


class SQLiteSession:
    async def __aenter__(self):
        await self.init()
        await self.enter()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.exit()

    async def init(self):
        logger.info("Initializing SQLite...")
        os.makedirs(TEST_VOLUMES_TESTS_DATABASE_SQLITE, exist_ok=True)

        database_url = DATABASE_URL_SQLITE
        async_session.load(database_url)

        from sqlalchemy import event
        from sqlalchemy.engine import Engine

        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, _):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()  # pragma: no cover

        await init_table()

    async def enter(self):
        ...

    async def exit(self):
        ...
