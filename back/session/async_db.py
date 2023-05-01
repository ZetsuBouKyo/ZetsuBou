from back.settings import DatabaseType, setting  # noqa: F401
from sqlalchemy import event  # noqa: F401
from sqlalchemy.engine import Engine  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

database_type = setting.database_type
database_url = setting.database_url
echo = setting.database_echo

async_engine = create_async_engine(database_url, echo=echo)


async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# if database_type == DatabaseType.SQLITE:

#     @event.listens_for(Engine, "connect")
#     def set_sqlite_pragma(dbapi_connection, _):
#         cursor = dbapi_connection.cursor()
#         cursor.execute("PRAGMA foreign_keys=ON")
#         cursor.close()
