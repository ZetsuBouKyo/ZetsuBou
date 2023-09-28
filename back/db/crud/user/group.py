from typing import List

from sqlalchemy import delete, update
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
    async def update(cls, user_id: int, group_ids: List[int]):
        new_group_ids = set(group_ids)
        to_deleted_ids = set()
        async with async_session() as session:
            async with session.begin():
                rows = await session.execute(select(cls).where(cls.user_id == user_id))
                for row in rows.scalars().all():
                    user_group = UserGroup(**row.__dict__)
                    if user_group.group_id not in new_group_ids:
                        to_deleted_ids.add(user_group.id)
                    else:
                        new_group_ids.remove(user_group.group_id)
                while new_group_ids and to_deleted_ids:
                    new_group_id = new_group_ids.pop()
                    to_update_id = to_deleted_ids.pop()
                    await session.execute(
                        update(cls)
                        .where(cls.id == to_update_id)
                        .values(user_id=user_id, group_id=new_group_id)
                    )

                if new_group_ids:
                    for group_id in new_group_ids:
                        session.add(UserGroupBase(user_id=user_id, group_id=group_id))
                if to_deleted_ids:
                    for id in to_deleted_ids:
                        await session.execute(
                            delete(UserGroupBase).where(UserGroupBase.id == id)
                        )

        return True

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
