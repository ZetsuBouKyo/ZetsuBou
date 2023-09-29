from typing import Any, Union

from pydantic import BaseModel
from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from back.session.async_db import async_session
from back.settings import setting

from ...model import UserFrontSettings, UserFrontSettingsUpdateByUserId
from ...table import (
    UserFrontSettingsGalleryImageAutoPlayTimeInterval,
    UserFrontSettingsGalleryImagePreviewSize,
    UserFrontSettingsGalleryPreviewSize,
    UserFrontSettingsVideoPreviewSize,
)


class UserFrontSettingsParameter(BaseModel):
    instance: Any
    front_settings_key: str
    table_col: str


_parameters = [
    {
        "instance": UserFrontSettingsGalleryImageAutoPlayTimeInterval,
        "front_settings_key": "gallery_image_auto_play_time_interval",
        "table_col": "interval",
    },
    {
        "instance": UserFrontSettingsGalleryImagePreviewSize,
        "front_settings_key": "gallery_image_preview_size",
        "table_col": "size",
    },
    {
        "instance": UserFrontSettingsGalleryPreviewSize,
        "front_settings_key": "gallery_preview_size",
        "table_col": "size",
    },
    {
        "instance": UserFrontSettingsVideoPreviewSize,
        "front_settings_key": "video_preview_size",
        "table_col": "size",
    },
]


parameters = [UserFrontSettingsParameter(**p) for p in _parameters]

UserFrontSettingsParameterBase = Union[
    UserFrontSettingsGalleryImageAutoPlayTimeInterval,
    UserFrontSettingsGalleryImagePreviewSize,
    UserFrontSettingsGalleryPreviewSize,
    UserFrontSettingsVideoPreviewSize,
]


async def _update(
    session: Session, instance: UserFrontSettingsParameterBase, user_id: int, data: dict
):
    await session.execute(
        update(instance).where(instance.user_id == user_id).values(**data)
    )


async def _get(
    session: Session, instance: UserFrontSettingsParameterBase, user_id: int
) -> dict:
    rows = await session.execute(select(instance).where(instance.user_id == user_id))
    first = rows.scalars().first()
    if first is None:
        return {}
    return first.__dict__


async def get_user_front_settings_by_user_id(
    session: Session, user_id: int
) -> UserFrontSettings:
    s = {"user_id": user_id}
    for p in parameters:
        row = await _get(session, p.instance, user_id)
        s[p.front_settings_key] = row.get(p.table_col, None)

    return UserFrontSettings(**s)


async def init_user_front_settings(session: Session, user_id: int):
    default_settings = setting.get_app_user_front_settings(user_id)
    settings = await get_user_front_settings_by_user_id(session, user_id)
    settings = settings.model_dump()
    for p in parameters:
        key = p.front_settings_key
        if settings.get(key, None) is None:
            d = {p.table_col: default_settings.get(key), "user_id": user_id}
            data = p.instance(**d)
            session.add(data)


class CrudUserFrontSettings:
    @classmethod
    async def init(cls, user_id: int) -> bool:
        async with async_session() as session:
            async with session.begin():
                await init_user_front_settings(session, user_id)
        return True

    @classmethod
    async def get_row_by_user_id(cls, user_id: int) -> UserFrontSettings:
        async with async_session() as session:
            async with session.begin():
                user_front_settings = await get_user_front_settings_by_user_id(
                    session, user_id
                )
        return user_front_settings

    @classmethod
    async def update_by_user_id(cls, settings: UserFrontSettingsUpdateByUserId) -> bool:
        need_to_update = False
        async with async_session() as session:
            async with session.begin():
                s = settings.model_dump()
                for p in parameters:
                    front_settings_val = s.get(p.front_settings_key, None)
                    if front_settings_val is not None:
                        await _update(
                            session,
                            p.instance,
                            settings.user_id,
                            {
                                p.table_col: front_settings_val,
                                "user_id": settings.user_id,
                            },
                        )
                        need_to_update = True

                if need_to_update:
                    await session.commit()
        return True
