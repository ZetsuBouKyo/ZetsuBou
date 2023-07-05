from sqlalchemy import event  # noqa: F401
from sqlalchemy.engine import Engine  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from back.settings import DatabaseTypeEnum, setting  # noqa: F401

DATABASE_TYPE = setting.database_type
DATABASE_URL = setting.database_url
ECHO = setting.database_echo

if DATABASE_URL is not None:
    async_engine = create_async_engine(DATABASE_URL, echo=ECHO)
else:
    async_engine = None


async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# if DATABASE_TYPE == DatabaseTypeEnum.SQLITE:

#     @event.listens_for(Engine, "connect")
#     def set_sqlite_pragma(dbapi_connection, _):
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON")
#         cursor.close()
