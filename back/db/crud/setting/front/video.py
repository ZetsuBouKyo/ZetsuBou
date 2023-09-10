from typing import List, Union

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.expression import true

from back.session.async_db import async_session

from ....model import (
    SettingFrontVideo,
    SettingFrontVideoCategory,
    SettingFrontVideoInterpretation,
    SettingFrontVideoTagField,
    SettingFrontVideoUpdate,
    TagToken,
)
from ....table import (
    SettingFrontVideoCategoryBase,
    SettingFrontVideoTagFieldBase,
    TagTokenBase,
)
from ...base import get_all_rows_by_condition_order_by_id


class CrudSettingFrontVideo:
    @classmethod
    async def get(cls) -> SettingFrontVideo:
        category_ids = await get_all_rows_by_condition_order_by_id(
            SettingFrontVideoCategoryBase,
            SettingFrontVideoCategoryBase.enable == true(),
            SettingFrontVideoCategory,
        )
        tag_field_ids = await get_all_rows_by_condition_order_by_id(
            SettingFrontVideoTagFieldBase,
            SettingFrontVideoTagFieldBase.enable == true(),
            SettingFrontVideoTagField,
        )
        return SettingFrontVideo(
            category_ids=category_ids,
            tag_field_ids=tag_field_ids,
        )

    @classmethod
    async def get_interpretation(cls):
        limit = 100

        c_skip = 0
        categories = []
        tmp = await cls.startwith_category("", skip=c_skip, limit=limit)
        categories += tmp
        while tmp:
            c_skip += limit
            tmp = await cls.startwith_category("", skip=c_skip, limit=limit)
            categories += tmp

        t_skip = 0
        tag_fields = []
        tmp = await cls.startwith_tag_field("", skip=t_skip, limit=limit)
        tag_fields += tmp
        while tmp:
            t_skip += limit
            tmp = await cls.startwith_tag_field("", skip=t_skip, limit=limit)
            tag_fields += tmp
        return SettingFrontVideoInterpretation(
            categories=categories, tag_fields=tag_fields
        )

    @classmethod
    async def _startwith(
        cls,
        base: Union[SettingFrontVideoCategoryBase, SettingFrontVideoTagFieldBase],
        s: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[TagToken]:
        out = []
        async with async_session() as session:
            async with session.begin():
                statement = (
                    select(TagTokenBase.id, TagTokenBase.name)
                    .select_from(base)
                    .where(base.enable == true())
                    .join(TagTokenBase, TagTokenBase.id == base.token_id)
                    .where(TagTokenBase.name.ilike(f"{s}%"))
                    .offset(skip)
                    .limit(limit)
                    .order_by(TagTokenBase.name)
                )
                rows = await session.execute(statement)
                for row in rows.mappings():
                    out.append(TagToken(**row))
        return out

    @classmethod
    async def startwith_category(
        cls, s: str, skip: int = 0, limit: int = 100
    ) -> List[TagToken]:
        return await cls._startwith(
            SettingFrontVideoCategoryBase, s, skip=skip, limit=limit
        )

    @classmethod
    async def startwith_tag_field(
        cls, s: str, skip: int = 0, limit: int = 100
    ) -> List[TagToken]:
        return await cls._startwith(
            SettingFrontVideoTagFieldBase, s, skip=skip, limit=limit
        )

    @classmethod
    async def _token_exists(cls, session: AsyncSession, id: int):
        rows = await session.execute(select(TagTokenBase).where(TagTokenBase.id == id))
        first = rows.scalars().first()
        if first is None:
            raise HTTPException(status_code=404, detail=f"Token id: {id} not found")

    @classmethod
    async def _disable_tokens(
        cls,
        session: AsyncSession,
        ids: List[int],
        base: Union[SettingFrontVideoCategoryBase, SettingFrontVideoTagFieldBase],
        model: Union[SettingFrontVideoCategory, SettingFrontVideoTagField],
    ):
        rows = 1
        skip = 0
        limit = 100
        while rows:
            rows = await session.execute(select(base).offset(skip).limit(limit))
            skip += limit
            rows = rows.scalars().all()
            if len(rows) == 0:
                break
            for row in rows:
                row = model(**row.__dict__)
                if row.token_id not in ids and row.enable:
                    row.enable = False
                    await session.execute(
                        update(base).where(base.id == row.id).values(**row.model_dump())
                    )

    @classmethod
    async def _enable_tokens(
        cls,
        session: AsyncSession,
        ids: List[int],
        base: Union[SettingFrontVideoCategoryBase, SettingFrontVideoTagFieldBase],
        model: Union[SettingFrontVideoCategory, SettingFrontVideoTagField],
    ):
        for id in ids:
            await cls._token_exists(session, id)

            rows = await session.execute(select(base).where(base.token_id == id))
            first = rows.scalars().first()
            if first is None:
                row = base(token_id=id, enable=True)
                session.add(row)
            else:
                row = model(**first.__dict__)
                if not row.enable:
                    row.enable = True
                    await session.execute(
                        update(base)
                        .where(base.token_id == id)
                        .values(**row.model_dump())
                    )

    @classmethod
    async def _update_categories(
        cls, session: AsyncSession, setting: SettingFrontVideoUpdate
    ):
        await cls._enable_tokens(
            session,
            setting.category_ids,
            SettingFrontVideoCategoryBase,
            SettingFrontVideoCategory,
        )
        await cls._disable_tokens(
            session,
            setting.category_ids,
            SettingFrontVideoCategoryBase,
            SettingFrontVideoCategory,
        )

    @classmethod
    async def _update_tag_fields(
        cls, session: AsyncSession, setting: SettingFrontVideoUpdate
    ):
        await cls._enable_tokens(
            session,
            setting.tag_field_ids,
            SettingFrontVideoTagFieldBase,
            SettingFrontVideoTagField,
        )
        await cls._disable_tokens(
            session,
            setting.tag_field_ids,
            SettingFrontVideoTagFieldBase,
            SettingFrontVideoTagField,
        )

    @classmethod
    async def update(cls, setting: SettingFrontVideoUpdate) -> bool:
        async with async_session() as session:
            async with session.begin():
                await cls._update_categories(session, setting)
                await cls._update_tag_fields(session, setting)
        return True

    @classmethod
    async def reset(cls) -> bool:
        async with async_session() as session:
            async with session.begin():
                await cls._disable_tokens(
                    session,
                    [],
                    SettingFrontVideoCategoryBase,
                    SettingFrontVideoCategory,
                )
                await cls._disable_tokens(
                    session,
                    [],
                    SettingFrontVideoTagFieldBase,
                    SettingFrontVideoTagField,
                )
        return True
