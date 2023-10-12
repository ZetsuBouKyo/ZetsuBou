from typing import List

from fastapi import HTTPException
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from back.model.scope import ScopeEnum
from back.session.async_db import async_session

from ...model import (
    Group,
    GroupCreate,
    GroupCreated,
    GroupUpdate,
    GroupWithScopeIdsSafeCreate,
    GroupWithScopeIdsUpdate,
    GroupWithScopeRow,
    GroupWithScopes,
    ScopeGroup,
)
from ...table import GroupBase, ScopeBase, ScopeGroupBase
from ..base import (
    count_total,
    create,
    delete_by_id,
    get_row_by,
    get_rows_order_by_id,
    overwrite_relation_between_tables,
    update_by_id,
)


async def overwrite_relation_between_scope_and_group(
    session: Session,
    group: GroupWithScopeIdsUpdate,
    scope_group_base: ScopeGroupBase = ScopeGroupBase,
    scope_group_model: ScopeGroup = ScopeGroup,
):
    return await overwrite_relation_between_tables(
        session,
        group,
        "group_id",
        "scope_ids",
        "scope_id",
        scope_group_base,
        scope_group_base.group_id,
        scope_group_model,
    )


async def get_group_with_scopes_by_id(
    session: Session,
    id: int,
    scope_base: ScopeBase = ScopeBase,
    group_base: GroupBase = GroupBase,
    scope_group_base: ScopeGroupBase = ScopeGroupBase,
) -> GroupWithScopes:
    statement = (
        select(
            group_base.id,
            group_base.name,
            scope_group_base.scope_id,
            scope_base.name.label("scope_name"),
        )
        .where(group_base.id == id)
        .outerjoin(scope_group_base, group_base.id == scope_group_base.group_id)
        .outerjoin(scope_base, scope_base.id == scope_group_base.scope_id)
    )
    _rows = await session.execute(statement)
    group = None
    for row in _rows.mappings():
        g = GroupWithScopeRow(**row)
        if group is None:
            scope_ids = []
            scope_names = []

            group = GroupWithScopes(
                id=g.id,
                name=g.name,
                scope_ids=scope_ids,
                scope_names=scope_names,
            )
        if g.scope_id is not None and g.scope_name is not None:
            group.scope_ids.append(g.scope_id)
            group.scope_names.append(g.scope_name)
    return group


class CrudGroup(GroupBase):
    @classmethod
    async def create(cls, group: GroupCreate) -> GroupCreated:
        return GroupCreated(**await create(cls, group))

    @classmethod
    async def safe_create_with_scope_ids(
        cls, group: GroupWithScopeIdsSafeCreate
    ) -> GroupWithScopes:
        async with async_session() as session:
            async with session.begin():
                rows = await session.execute(select(cls).where(cls.name == group.name))
                first = rows.scalars().first()
                if first is None:
                    first = cls(name=group.name)
                    session.add(cls(name=group.name))
                    await session.flush()
                    rows = await session.execute(
                        select(cls).where(cls.name == group.name)
                    )
                    first = rows.scalars().first()

                group_to_update = GroupWithScopeIdsUpdate(
                    id=first.id, name=group.name, scope_ids=group.scope_ids
                )
                await overwrite_relation_between_scope_and_group(
                    session, group_to_update
                )
                group = await get_group_with_scopes_by_id(session, group_to_update.id)
        return group

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> Group:
        return await get_row_by(cls, cls.id == id, Group)

    @classmethod
    async def get_row_with_scopes_by_id(cls, id: int) -> GroupWithScopes:
        async with async_session() as session:
            async with session.begin():
                group = await get_group_with_scopes_by_id(session, id)
        return group

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
    async def update_with_scope_ids_by_id(cls, group: GroupWithScopeIdsUpdate) -> bool:
        async with async_session() as session:
            async with session.begin():
                await overwrite_relation_between_scope_and_group(session, group)
        return True

    @classmethod
    async def update_by_id(cls, group: GroupUpdate) -> bool:
        return await update_by_id(cls, group)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        admin_group = await cls.get_row_by_name(ScopeEnum.admin.value)
        if admin_group.id == id:
            raise HTTPException(
                status_code=101,
                detail=f"You don't have permission for deleting group id: {id} group name: {ScopeEnum.admin.value}",
            )
        return await delete_by_id(cls, id)
