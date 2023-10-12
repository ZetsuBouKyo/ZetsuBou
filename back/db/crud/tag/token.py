from typing import List

from sqlalchemy import desc
from sqlalchemy.future import select

from back.session.async_db import async_session

from ...model import TagToken, TagTokenCreate, TagTokenCreated, TagTokenUpdate
from ...table import TagCategoryBase, TagTokenBase
from ..base import (
    count_total,
    create,
    delete_by_id,
    get_row_by,
    get_row_by_id,
    get_rows_by_condition_order_by,
    get_rows_by_ids_order_by_id,
    get_rows_order_by_id,
    update_by_id,
)


class CrudTagToken(TagTokenBase):
    @classmethod
    async def create(cls, token: TagTokenCreate) -> TagTokenCreated:
        return TagTokenCreated(**await create(cls, token))

    @classmethod
    async def count_total(cls) -> int:
        return await count_total(cls)

    @classmethod
    async def exists(cls, id: int) -> bool:
        return await cls.get_row_by_id(id) is not None

    @classmethod
    async def get_row_by_id(cls, id: int) -> TagToken:
        return await get_row_by_id(cls, id, TagToken)

    @classmethod
    async def get_row_by_name(cls, name: str) -> TagToken:
        return await get_row_by(cls, cls.name == name, TagToken)

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagToken]:
        return await get_rows_order_by_id(
            cls, TagToken, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def get_rows_by_ids_order_by_id(
        cls, ids: List[int], skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagToken]:
        return await get_rows_by_ids_order_by_id(
            cls, ids, TagToken, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def startswith(
        cls, s: str, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[TagToken]:
        return await get_rows_by_condition_order_by(
            cls,
            cls.name.ilike(f"{s}%"),
            cls.name,
            TagToken,
            skip=skip,
            limit=limit,
            is_desc=is_desc,
        )

    @classmethod
    async def startswith_by_category(
        cls,
        s: str,
        category: str,
        skip: int = 0,
        limit: int = 100,
        is_desc: bool = False,
    ) -> List[TagToken]:
        out = []
        order = cls.name
        if is_desc:
            order = desc(order)
        async with async_session() as session:
            async with session.begin():
                rows = await session.execute(select(cls.id).where(cls.name == category))
                category_id = rows.scalars().first()
                if category_id is None:
                    return []

                statement = (
                    select(cls.id, cls.name)
                    .select_from(TagCategoryBase)
                    .where(TagCategoryBase.linked_id == category_id)
                    .join(cls, cls.id == TagCategoryBase.token_id)
                    .where(cls.name.ilike(f"{s}%"))
                    .offset(skip)
                    .limit(limit)
                    .order_by(order)
                )
                rows = await session.execute(statement)
            if rows is None:
                return out
            for row in rows.mappings():
                out.append(TagToken(**row))
        return out

    @classmethod
    async def startswith_by_category_id(
        cls,
        s: str,
        category_id: int,
        skip: int = 0,
        limit: int = 100,
        is_desc: bool = False,
    ) -> List[TagToken]:
        out = []
        order = cls.name
        if is_desc:
            order = desc(order)
        async with async_session() as session:
            async with session.begin():
                statement = (
                    select(cls.id, cls.name)
                    .select_from(TagCategoryBase)
                    .where(TagCategoryBase.linked_id == category_id)
                    .join(cls, cls.id == TagCategoryBase.token_id)
                    .where(cls.name.ilike(f"{s}%"))
                    .offset(skip)
                    .limit(limit)
                    .order_by(order)
                )
                rows = await session.execute(statement)
            if rows is None:
                return out
            for row in rows.mappings():
                out.append(TagToken(**row))
        return out

    @classmethod
    async def update_by_id(cls, token: TagTokenUpdate) -> bool:
        return await update_by_id(cls, token)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
