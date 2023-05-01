from sqlalchemy.sql import functions as func

from ...model import (
    UserFrontSetting,
    UserFrontSettingCreate,
    UserFrontSettingCreated,
    UserFrontSettingUpdateByUserId,
)
from ...table import UserFrontSettingBase
from ..base import create, delete_by, get_row_by, update_by_instance


class CrudUserFrontSetting(UserFrontSettingBase):
    @classmethod
    async def create(
        cls, user_front_setting: UserFrontSettingCreate
    ) -> UserFrontSettingCreated:
        return UserFrontSettingCreated(**await create(cls, user_front_setting))

    @classmethod
    async def get_row_by_user_id(cls, user_id: int) -> UserFrontSetting:
        return await get_row_by(cls, cls.user_id == user_id, UserFrontSetting)

    @classmethod
    async def update_by_user_id(
        cls, user_front_setting: UserFrontSettingUpdateByUserId
    ) -> bool:
        user_front_setting_modified = user_front_setting.dict()
        user_front_setting_modified["modified"] = func.now()
        return await update_by_instance(
            cls, cls.user_id == user_front_setting.user_id, user_front_setting_modified
        )

    @classmethod
    async def delete_by_user_id(cls, user_id: int):
        return await delete_by(cls, cls.user_id == user_id)
