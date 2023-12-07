from typing import List, Optional

from sqlalchemy import delete

from back.model.scope import ScopeEnum
from back.session.async_db import async_session

from ...model import Scope, ScopeCreate, ScopeCreated, ScopeUpdate
from ...table import ScopeBase
from ..base import (
    create,
    delete_by_id,
    get_all_rows_order_by_id,
    get_row_by,
    get_row_by_id,
    get_rows_by_condition_order_by,
    get_rows_order_by_id,
    update_by_id,
)


class CrudScope(ScopeBase):
    @classmethod
    async def create(cls, token: ScopeCreate) -> ScopeCreated:
        return ScopeCreated(**await create(cls, token))

    @classmethod
    async def startswith(
        cls, name: str, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[Scope]:
        return await get_rows_by_condition_order_by(
            cls,
            cls.name.ilike(f"{name}%"),
            cls.name,
            Scope,
            skip=skip,
            limit=limit,
            is_desc=is_desc,
        )

    @classmethod
    async def get_row_by_id(cls, id: int) -> Optional[Scope]:
        return await get_row_by_id(cls, id, Scope)

    @classmethod
    async def get_row_by_name(cls, name: str) -> Optional[Scope]:
        name = name.lower()
        return await get_row_by(cls, cls.name == name, Scope)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[Scope]:
        return await get_rows_order_by_id(
            cls, Scope, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def get_all_rows_order_by_id(cls) -> List[dict]:
        return await get_all_rows_order_by_id(cls)

    @classmethod
    async def init(cls, scope_enum: ScopeEnum = ScopeEnum) -> bool:
        scopes_in_db = await cls.get_all_rows_order_by_id()
        scope_values_in_db = {s.get("name", None) for s in scopes_in_db}
        scope_values = {s.value for s in scope_enum}
        _to_add = scope_values - scope_values_in_db
        to_add = list(_to_add)
        to_add.sort()
        _to_delete = scope_values_in_db - scope_values
        to_delete = list(_to_delete)
        to_delete.sort()

        async with async_session() as session:
            async with session.begin():
                for scope_name in to_add:
                    session.add(cls(name=scope_name))
                for scope_name in to_delete:
                    await session.execute(delete(cls).where(cls.name == scope_name))
        return True

    @classmethod
    async def update_by_id(cls, scope: ScopeUpdate) -> bool:
        return await update_by_id(cls, scope)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
