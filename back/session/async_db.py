from typing import Any

from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from back.settings import DatabaseTypeEnum, setting

DATABASE_TYPE = setting.database_type
DATABASE_URL = setting.database_url
ECHO = setting.database_echo


class DatabaseSession:
    def __init__(
        self,
        database_url: str,
        echo: bool = ECHO,
        expire_on_commit: bool = False,
        class_: AsyncSession = AsyncSession,
    ):
        self.async_engine = create_async_engine(database_url, echo=echo)
        self.expire_on_commit = expire_on_commit
        self.class_ = class_

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return sessionmaker(
            self.async_engine,
            *args,
            expire_on_commit=self.expire_on_commit,
            class_=self.class_,
            **kwargs
        )()

    def load(
        self,
        database_url: str,
        echo: bool = ECHO,
        expire_on_commit: bool = False,
        class_: AsyncSession = AsyncSession,
    ):
        self.async_engine = create_async_engine(database_url, echo=echo)
        self.expire_on_commit = expire_on_commit
        self.class_ = class_


async_session = DatabaseSession(
    DATABASE_URL, echo=ECHO, expire_on_commit=False, class_=AsyncSession
)

if DATABASE_TYPE == DatabaseTypeEnum.SQLITE:

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, _):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
