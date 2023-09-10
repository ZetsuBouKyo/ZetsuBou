from typing import List

from sqlalchemy.future import select

from back.session.async_db import async_session

from ...model import UserGroup, UserGroupCreate
from ...table import GroupBase, UserBase, UserGroupBase
from ..base import (
    create,
    delete_by_id,
    get_row_by,
    get_rows_by_condition_order_by_id,
    get_rows_order_by_id,
)


class CrudUserGroup(UserGroupBase):
    @classmethod
    async def create(cls, user_group: UserGroupCreate) -> UserGroup:
        return UserGroup(**await create(cls, user_group))

    @classmethod
    async def batch_create(cls, user_groups: List[UserGroupCreate]):
        out = []
        async with async_session() as session:
            for group in user_groups:
                rows = await session.execute(
                    select(UserBase).where(UserBase.id == group.user_id)
                )
                first = rows.scalars().first()
                if first is None:
                    session.rollback()
                    return []

                rows = await session.execute(
                    select(GroupBase).where(GroupBase.id == group.group_id)
                )
                first = rows.scalars().first()
                if first is None:
                    session.rollback()
                    return []

                inst = cls(**group.model_dump())
                session.add(inst)
                await session.flush()
                out.append(inst.__dict__)
            session.commit()
        return out

    @classmethod
    async def get_row_by_id(cls, id: int) -> UserGroup:
        return await get_row_by(cls, cls.id == id, UserGroup)

    @classmethod
    async def get_rows_by_group_id_order_by_id(cls, group_id: int) -> List[UserGroup]:
        return await get_rows_by_condition_order_by_id(
            cls, cls.group_id == group_id, UserGroup, limit=1
        )

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserGroup]:
        return await get_rows_order_by_id(
            cls, UserGroup, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
