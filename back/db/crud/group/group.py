from typing import List

from back.session.async_db import async_session
from fastapi import HTTPException
from sqlalchemy import and_, delete, update

from ...model import (
    Group,
    GroupCreate,
    GroupCreated,
    GroupCreatedWithScopes,
    GroupCreateWithScopes,
    GroupUpdateWithScopes,
    GroupWithScopes,
    Scope,
    ScopeEnum,
)
from ...table import GroupBase, ScopeBase
from ..base import (
    count_total,
    create,
    delete_by_id,
    get_row_by,
    get_rows_order_by_id,
    iter_by_condition_order_by_id,
)


class CrudGroup(GroupBase):
    @classmethod
    async def create(cls, group: GroupCreate) -> GroupCreated:
        return GroupCreated(**await create(cls, group))

    @classmethod
    async def create_with_scopes(
        cls, group_with_scopes: GroupCreateWithScopes
    ) -> GroupCreatedWithScopes:
        async with async_session() as session:
            async with session.begin():
                group = cls(name=group_with_scopes.name)
                session.add(group)
                await session.flush()

                for scope_id in group_with_scopes.scope_ids:
                    inst = ScopeBase(id=scope_id, group_id=group.id)
                    session.add(inst)
                    await session.flush()

        return GroupCreatedWithScopes(
            id=group.id, name=group.name, scope_ids=group_with_scopes.scope_ids
        )

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def get_row_by_id(cls, id: int) -> Group:
        return await get_row_by(cls, cls.id == id, Group)

    @classmethod
    async def get_row_with_scopes_by_id(cls, id: int) -> GroupWithScopes:
        group = await cls.get_row_by_id(id)
        if group is None:
            return None
        group_with_scopes = GroupWithScopes(id=id, name=group.name, scope_ids=[])
        async for scopes in iter_by_condition_order_by_id(
            ScopeBase, ScopeBase.group_id == id, Scope
        ):
            for scope in scopes:
                group_with_scopes.scope_ids.append(scope.id)
        return group_with_scopes

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
    async def update_with_scopes(cls, group_with_scopes: GroupUpdateWithScopes) -> bool:
        old_group_with_scopes = await cls.get_row_with_scopes_by_id(
            group_with_scopes.id
        )
        old_scope_ids = set(old_group_with_scopes.scope_ids)
        new_scope_ids = set(group_with_scopes.scope_ids)

        scope_ids_to_delete = old_scope_ids - new_scope_ids
        scope_ids_to_delete = list(scope_ids_to_delete)
        scope_ids_to_delete.sort()

        scope_ids_to_add = new_scope_ids - old_scope_ids
        scope_ids_to_add = list(scope_ids_to_add)
        scope_ids_to_add.sort()
        async with async_session() as session:
            rows = await session.execute(
                update(cls)
                .where(cls.id == group_with_scopes.id)
                .values(id=group_with_scopes.id, name=group_with_scopes.name)
            )
            await session.flush()
            if rows.rowcount != 1:
                return False

            for scope_id in scope_ids_to_add:
                inst = ScopeBase(id=scope_id, group_id=group_with_scopes.id)
                session.add(inst)
                await session.flush()

            for scope_id in scope_ids_to_delete:
                rows = await session.execute(
                    delete(ScopeBase).where(
                        and_(
                            ScopeBase.id == scope_id,
                            ScopeBase.group_id == group_with_scopes.id,
                        )
                    )
                )
                await session.flush()
            await session.commit()
        return True

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        admin_group = await cls.get_row_by_name(ScopeEnum.admin.name)
        if admin_group.id == id:
            raise HTTPException(
                status_code=101,
                detail=f"You don't have permission for deleting group id: {id} group "
                f"name: {ScopeEnum.admin.name}",
            )
        return await delete_by_id(cls, id)
