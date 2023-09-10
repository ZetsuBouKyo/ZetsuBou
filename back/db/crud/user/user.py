from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.sql import functions as func

from back.security import get_hashed_password, verify_password
from back.session.async_db import async_session

from ...crud import CrudUserFrontSettings
from ...model import Group, User, UserCreate, UserCreated, UserUpdate
from ...table import GroupBase, UserBase, UserGroupBase
from ..base import (
    batch_create,
    count_total,
    delete_all,
    delete_by,
    delete_by_id,
    get_row_by,
    get_row_by_id,
    get_rows_order_by_id,
)


def get_user_hashed_password(user: BaseModel) -> dict:
    user = user.model_dump()
    user["hashed_password"] = get_hashed_password(user["password"])
    del user["password"]
    return user


class CrudUser(UserBase):
    @classmethod
    async def create(
        cls, user: UserCreate, is_front_settings: bool = True
    ) -> UserCreated:
        user = get_user_hashed_password(user)
        async with async_session() as session:
            instance = cls(**user)
            async with session.begin():
                session.add(instance)

                await session.flush()
                created_user = UserCreated(**instance.__dict__)
        if created_user is None or not created_user.id:
            raise HTTPException(
                status_code=500, detail="Internal Server Error: sqlalchemy create user"
            )
        if is_front_settings:
            await CrudUserFrontSettings.init(created_user.id)

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
    async def update_by_user(cls, user: UserUpdate) -> bool:
        async with async_session() as session:
            async with session.begin():
                row = await session.execute(select(cls).where(cls.email == user.email))
                first = row.scalars().first()
                if first is None:
                    raise HTTPException(status_code=401, detail="Not authenticated")
            async with session.begin():
                if not verify_password(user.password, first.hashed_password):
                    raise HTTPException(status_code=401, detail="Not authenticated")

                new_user = {}
                if user.name is not None and user.name != first.name:
                    new_user["name"] = user.name
                if user.new_password is not None:
                    new_user["hashed_password"] = get_hashed_password(user.new_password)

                if new_user:
                    rows = await session.execute(
                        update(cls).where(cls.email == first.email).values(**new_user)
                    )
                    await session.commit()
                    if rows.rowcount == 0:
                        raise HTTPException(status_code=500, detail="Update failed")
            async with session.begin():
                row = await session.execute(select(cls).where(cls.email == user.email))
                first = row.scalars().first()
        return User(**first.__dict__)

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
                    else:
                        return None
                else:
                    return None

        return User(**first.__dict__)
