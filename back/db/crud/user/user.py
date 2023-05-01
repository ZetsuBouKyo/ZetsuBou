from typing import List

from back.security import get_hashed_password, verify_password
from back.session.async_db import async_session
from back.settings import setting
from pydantic import BaseModel, EmailStr
from sqlalchemy.future import select
from sqlalchemy.sql import functions as func

from ...model import Group, User, UserCreate, UserCreated
from ...table import GroupBase, UserBase, UserFrontSettingBase, UserGroupBase
from ..base import (
    batch_create,
    count_total,
    delete_all,
    delete_by,
    delete_by_id,
    get_row_by,
    get_row_by_id,
    get_rows_order_by_id,
    update_by_id,
)


def get_user_hashed_password(user: BaseModel) -> dict:
    user = user.dict()
    user["hashed_password"] = get_hashed_password(user["password"])
    del user["password"]
    return user


class CrudUser(UserBase):
    @classmethod
    async def create(cls, user: UserCreate) -> UserCreated:
        user = get_user_hashed_password(user)
        async with async_session() as session:
            instance = cls(**user)
            async with session.begin():
                session.add(instance)

                await session.flush()
                created_user = UserCreated(**instance.__dict__)

                template_front_setting = setting.app_user_front_setting
                template_front_setting["user_id"] = created_user.id
                session.add(UserFrontSettingBase(**template_front_setting))
        return created_user

    @classmethod
    async def batch_create(cls, users: List[UserCreate]):
        for i in range(len(users)):
            users[i] = get_user_hashed_password(users[i])
        return await batch_create(cls, users)

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> User:
        return await get_row_by_id(cls, id, User)

    @classmethod
    async def get_row_by_email(cls, email: EmailStr) -> User:
        return await get_row_by(cls, cls.email == email, User)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[User]:
        return await get_rows_order_by_id(
            cls, User, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def get_groups_by_id(cls, id: int) -> List[Group]:
        out = []
        async with async_session() as session:
            async with session.begin():
                statement = (
                    select(GroupBase)
                    .select_from(cls)
                    .where(cls.id == id)
                    .join(UserGroupBase)
                    .join(GroupBase)
                )

                rows = await session.execute(statement)
                if rows is None:
                    return out

                for row in rows.scalars().all():
                    out.append(Group(**row.__dict__))
        return out

    @classmethod
    async def update_by_id(cls, user) -> bool:
        user = get_user_hashed_password(user)
        return await update_by_id(cls, user)

    @classmethod
    async def delete_all(cls):
        return await delete_all(cls)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)

    @classmethod
    async def delete_by_email(cls, email: EmailStr) -> bool:
        return await delete_by(cls, cls.email == email)

    @classmethod
    async def verify(cls, email: EmailStr, password: str) -> User:
        first = None
        async with async_session() as session:
            async with session.begin():
                row = await session.execute(select(cls).where(cls.email == email))
                first = row.scalars().first()
            async with session.begin():
                if first is not None:
                    if verify_password(password, first.hashed_password):
                        first.last_signin = func.now()

                        row = await session.execute(
                            select(cls).where(cls.email == email)
                        )
                        first = row.scalars().first()
        if first is None:
            return None
        return User(**first.__dict__)
