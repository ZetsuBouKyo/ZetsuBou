from typing import List, Optional, Union

from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import delete, desc, update
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from sqlalchemy.sql import functions as func

from back.security import get_hashed_password, verify_password
from back.session.async_db import async_session

from ...model import (
    Group,
    User,
    UserCreate,
    UserCreated,
    UserGroup,
    UserUpdate,
    UserWithGroupAndHashedPassword,
    UserWithGroupAndHashedPasswordRow,
    UserWithGroupRow,
    UserWithGroups,
    UserWithGroupsCreate,
    UserWithGroupsCreated,
    UserWithGroupsUpdate,
    UserWithHashedPassword,
)
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
from .front_settings import init_user_front_settings
from .group import update_group_ids_by_user_id


def get_user_hashed_password(user: Union[UserCreate, UserWithGroupsCreate]) -> dict:
    u = {}
    u.update(name=user.name)
    u.update(email=user.email)
    u.update(hashed_password=get_hashed_password(user.password))
    return u


class _CrudUser:
    def __init__(
        self,
        session: Session,
        base: UserBase,
        user_id: int,
        user: Union[UserUpdate, UserWithGroupsUpdate],
        user_group_base: UserGroupBase = UserGroupBase,
        group_base: GroupBase = GroupBase,
    ):
        self.session = session
        self.base = base
        self.user_id = user_id
        self.user = user
        self.user_group_base = user_group_base
        self.group_base = group_base

        self.new_user = {}
        self.with_group = type(user) == UserWithGroupsUpdate

    async def get_user_in_db(self):
        if not self.with_group:
            row = await self.session.execute(
                select(self.base).where(self.base.id == self.user_id)
            )
            user_in_db = row.scalars().first()
            if user_in_db is None:
                raise HTTPException(status_code=401, detail="Not authenticated")
        else:
            statement = (
                select(
                    self.base.id,
                    self.base.name,
                    self.base.email,
                    self.base.created,
                    self.base.last_signin,
                    self.base.hashed_password,
                    self.user_group_base.group_id,
                )
                .where(self.base.id == self.user_id)
                .outerjoin(
                    self.user_group_base, self.base.id == self.user_group_base.user_id
                )
            )
            _rows = await self.session.execute(statement)
            user_in_db = None
            for row in _rows.mappings():
                r = UserWithGroupAndHashedPasswordRow(**row)
                if user_in_db is None:
                    group_ids = []
                    group_names = []

                    user_in_db = UserWithGroupAndHashedPassword(
                        id=r.id,
                        name=r.name,
                        email=r.email,
                        created=r.created,
                        last_signin=r.last_signin,
                        group_ids=group_ids,
                        group_names=group_names,
                        hashed_password=r.hashed_password,
                    )
                if r.group_id is not None and r.group_name is not None:
                    user_in_db.group_ids.append(r.group_id)
                    user_in_db.group_names.append(r.group_name)

        return user_in_db

    async def get_updated_user(self):
        updated_user = {}
        if not self.with_group:
            row = await self.session.execute(
                select(self.base).where(self.base.id == self.user_id)
            )
            first = row.scalars().first()
            updated_user = first.__dict__
            updated_user = User(**updated_user)
        else:
            statement = (
                select(
                    self.base.id,
                    self.base.name,
                    self.base.email,
                    self.base.created,
                    self.base.last_signin,
                    self.user_group_base.group_id,
                    self.group_base.name.label("group_name"),
                )
                .where(self.base.id == self.user_id)
                .outerjoin(
                    self.user_group_base, self.base.id == self.user_group_base.user_id
                )
                .outerjoin(
                    self.group_base, self.group_base.id == self.user_group_base.group_id
                )
            )
            _rows = await self.session.execute(statement)
            updated_user = None
            for row in _rows.mappings():
                r = UserWithGroupRow(**row)
                if updated_user is None:
                    group_ids = []
                    group_names = []
                    updated_user = UserWithGroups(
                        id=r.id,
                        name=r.name,
                        email=r.email,
                        created=r.created,
                        last_signin=r.last_signin,
                        group_ids=group_ids,
                        group_names=group_names,
                    )
                if r.group_id is not None and r.group_name is not None:
                    updated_user.group_ids.append(r.group_id)
                    updated_user.group_names.append(r.group_name)

        return updated_user

    async def is_email(self):
        new_user_email = self.user.email
        if new_user_email != self.user_in_db.email:
            row = await self.session.execute(
                select(self.base).where(self.base.email == new_user_email)
            )
            user_check_email = row.scalars().first()
            if user_check_email is not None:
                raise HTTPException(
                    status_code=409, detail=f"{new_user_email} already exists"
                )
            self.new_user.update(email=new_user_email)

    async def _update(self):
        if self.user.name is not None and self.user.name != self.user_in_db.name:
            self.new_user.update(name=self.user.name)
        if self.user.new_password is not None:
            self.new_user.update(
                hashed_password=get_hashed_password(self.user.new_password)
            )

        if self.new_user:
            rows = await self.session.execute(
                update(self.base)
                .where(self.base.id == self.user_in_db.id)
                .values(**self.new_user)
            )
            if rows.rowcount == 0:
                raise HTTPException(status_code=500, detail="Update failed")

        if self.with_group:
            if len(self.user.group_ids) == 0:
                await self.session.execute(
                    delete(self.user_group_base).where(
                        self.user_group_base.user_id == self.user_id
                    )
                )
            else:
                await update_group_ids_by_user_id(
                    self.session,
                    self.user_id,
                    self.user.group_ids,
                    user_group_base=self.user_group_base,
                )

    async def update(self) -> Union[User, UserWithGroups]:
        self.user_in_db = await self.get_user_in_db()
        if self.user_in_db is None:
            raise HTTPException(status_code=404, detail="User does not exist")

        if not verify_password(self.user.password, self.user_in_db.hashed_password):
            raise HTTPException(status_code=401, detail="Not authenticated")

        await self.is_email()
        await self._update()

        updated_user = await self.get_updated_user()
        if updated_user is None:
            raise HTTPException(status_code=500, detail="Update failed")

        return updated_user


async def create_user(
    session: Session,
    user: Union[UserCreate, UserWithGroupsCreate],
    user_base: UserBase = UserBase,
    is_front_settings: bool = True,
) -> UserCreated:
    user_dict = get_user_hashed_password(user)
    instance = user_base(**user_dict)

    session.add(instance)
    await session.flush()
    created_user = UserCreated(**instance.__dict__)

    if is_front_settings:
        await init_user_front_settings(session, created_user.id)
    return created_user


async def get_user_with_groups_by_id(
    session: Session,
    id: int,
    user_base: UserBase = UserBase,
    user_group_base: UserGroupBase = UserGroupBase,
    group_base: GroupBase = GroupBase,
) -> Optional[UserWithGroups]:
    statement = (
        select(
            user_base.id,
            user_base.name,
            user_base.email,
            user_base.created,
            user_base.last_signin,
            user_group_base.group_id,
            group_base.name.label("group_name"),
        )
        .where(user_base.id == id)
        .outerjoin(user_group_base, user_base.id == user_group_base.user_id)
        .outerjoin(group_base, group_base.id == user_group_base.group_id)
    )
    _rows = await session.execute(statement)
    user = None
    for row in _rows.mappings():
        r = UserWithGroupRow(**row)
        if user is None:
            group_ids = []
            group_names = []

            user = UserWithGroups(
                id=r.id,
                name=r.name,
                email=r.email,
                created=r.created,
                last_signin=r.last_signin,
                group_ids=group_ids,
                group_names=group_names,
            )
        if r.group_id is not None and r.group_name is not None:
            user.group_ids.append(r.group_id)
            user.group_names.append(r.group_name)
    return user


class CrudUser(UserBase):
    @classmethod
    async def create(
        cls, user: UserCreate, is_front_settings: bool = True
    ) -> UserCreated:
        async with async_session() as session:
            async with session.begin():
                created_user = await create_user(
                    session, user, user_base=cls, is_front_settings=is_front_settings
                )

        return created_user

    @classmethod
    async def create_with_groups(
        cls, user: UserWithGroupsCreate, is_front_settings: bool = True
    ) -> UserWithGroupsCreated:
        async with async_session() as session:
            async with session.begin():
                created_user = await create_user(
                    session, user, user_base=cls, is_front_settings=is_front_settings
                )
                await update_group_ids_by_user_id(
                    session,
                    created_user.id,
                    user.group_ids,
                    user_group_base=UserGroupBase,
                )

                rows = await session.execute(
                    select(UserGroupBase).where(
                        UserGroupBase.user_id == created_user.id
                    )
                )
                user_group_ids = []
                for row in rows.scalars().all():
                    user_group = UserGroup(**row.__dict__)
                    user_group_ids.append(user_group.group_id)

                created_user_with_groups_dict = created_user.model_dump()
                created_user_with_groups_dict.update(group_ids=user_group_ids)
        return UserWithGroupsCreated(**created_user_with_groups_dict)

    @classmethod
    async def batch_create(cls, users: List[UserCreate]):
        for i in range(len(users)):
            users[i] = get_user_hashed_password(users[i])
        return await batch_create(cls, users)

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> Optional[User]:
        return await get_row_by_id(cls, id, User)

    @classmethod
    async def get_row_with_groups_by_id(cls, id: int) -> Optional[UserWithGroups]:
        async with async_session() as session:
            async with session.begin():
                user = await get_user_with_groups_by_id(session, id, user_base=cls)
        return user

    @classmethod
    async def get_row_by_email(cls, email: EmailStr) -> Optional[User]:
        return await get_row_by(cls, cls.email == email, User)

    @classmethod
    async def get_row_with_hashed_password_by_email(
        cls, email: EmailStr
    ) -> Optional[UserWithHashedPassword]:
        return await get_row_by(cls, cls.email == email, UserWithHashedPassword)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[User]:
        return await get_rows_order_by_id(
            cls, User, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def get_rows_with_group_id_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserWithGroups]:
        out = []
        order = cls.id
        if is_desc:
            order = desc(cls.id)
        async with async_session() as session:
            async with session.begin():
                sub_statement = (
                    select(cls).offset(skip).limit(limit).order_by(order).subquery()
                )

                statement = (
                    select(
                        cls.id,
                        cls.name,
                        cls.email,
                        cls.created,
                        cls.last_signin,
                        UserGroupBase.group_id,
                        GroupBase.name.label("group_name"),
                    )
                    .select_from(cls)
                    .join(sub_statement, sub_statement.c.id == cls.id)
                    .outerjoin(
                        UserGroupBase, sub_statement.c.id == UserGroupBase.user_id
                    )
                    .outerjoin(GroupBase, GroupBase.id == UserGroupBase.group_id)
                    .order_by(order)
                )
                rows = await session.execute(statement)
                for row in rows.mappings():
                    r = UserWithGroupRow(**row)
                    if len(out) > 0:
                        last: UserWithGroups = out[-1]
                        if (
                            (last.id == r.id)
                            and r.group_id is not None
                            and r.group_name is not None
                        ):
                            last.group_ids.append(r.group_id)
                            last.group_names.append(r.group_name)
                            continue

                    group_ids = []
                    group_names = []
                    if r.group_id is not None and r.group_name is not None:
                        group_ids.append(r.group_id)
                        group_names.append(r.group_name)
                    out.append(
                        UserWithGroups(
                            id=r.id,
                            name=r.name,
                            email=r.email,
                            created=r.created,
                            last_signin=r.last_signin,
                            group_ids=group_ids,
                            group_names=group_names,
                        )
                    )
        return out

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
    async def update_by_user(cls, user_id: int, user: UserUpdate) -> User:
        async with async_session() as session:
            async with session.begin():
                crud = _CrudUser(session, cls, user_id, user)
                updated_user = await crud.update()
        return updated_user

    @classmethod
    async def update_by_user_with_group(
        cls, user_id: int, user: UserWithGroupsUpdate
    ) -> UserWithGroups:
        async with async_session() as session:
            async with session.begin():
                crud = _CrudUser(session, cls, user_id, user)
                updated_user = await crud.update()
        return updated_user

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
    async def verify(cls, email: EmailStr, password: str) -> Optional[UserWithGroups]:
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
            async with session.begin():
                user = await get_user_with_groups_by_id(
                    session, first.id, user_base=cls
                )

        return user
