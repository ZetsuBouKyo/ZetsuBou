from typing import List

from fastapi import HTTPException

from back.model.scope import ScopeEnum

from ...model import Group, GroupCreate, GroupCreated
from ...table import GroupBase
from ..base import count_total, create, delete_by_id, get_row_by, get_rows_order_by_id


class CrudGroup(GroupBase):
    @classmethod
    async def create(cls, group: GroupCreate) -> GroupCreated:
        return GroupCreated(**await create(cls, group))

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> Group:
        return await get_row_by(cls, cls.id == id, Group)

    @classmethod
    async def get_row_by_name(cls, name: str) -> Group:
        name = name.lower()
        return await get_row_by(cls, cls.name == name, Group)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[Group]:
        return await get_rows_order_by_id(
            cls, Group, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        admin_group = await cls.get_row_by_name(ScopeEnum.admin.name)
        if admin_group.id == id:
            raise HTTPException(
                status_code=101,
                detail=f"You don't have permission for deleting group id: {id} group name: {ScopeEnum.admin.name}",
            )
        return await delete_by_id(cls, id)
