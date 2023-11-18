from logging import Logger

import pytest

from back.db.crud import CrudUserFrontSettings
from back.db.model import UserFrontSettingsUpdateByUserId
from tests.general.user import UserSession


@pytest.mark.asyncio
async def test_crud(logger: Logger):
    async with UserSession() as session:
        user_1 = session.created_user_with_groups

        user_front_settings_1_0 = await CrudUserFrontSettings.get_row_by_user_id(
            user_1.id
        )
        user_front_settings_1_1 = UserFrontSettingsUpdateByUserId(
            user_id=user_1.id,
            gallery_preview_size=user_front_settings_1_0.gallery_preview_size + 1,
            gallery_image_auto_play_time_interval=user_front_settings_1_0.gallery_image_auto_play_time_interval
            + 1,
            gallery_image_preview_size=user_front_settings_1_0.gallery_image_preview_size
            + 1,
            video_preview_size=user_front_settings_1_0.video_preview_size + 1,
        )

        await CrudUserFrontSettings.update_by_user_id(user_front_settings_1_1)

        user_front_settings_1_2 = await CrudUserFrontSettings.get_row_by_user_id(
            user_1.id
        )

        assert (
            user_front_settings_1_1.gallery_preview_size
            == user_front_settings_1_2.gallery_preview_size
        )
        assert (
            user_front_settings_1_1.gallery_image_auto_play_time_interval
            == user_front_settings_1_2.gallery_image_auto_play_time_interval
        )
        assert (
            user_front_settings_1_1.gallery_image_preview_size
            == user_front_settings_1_2.gallery_image_preview_size
        )
        assert (
            user_front_settings_1_1.video_preview_size
            == user_front_settings_1_2.video_preview_size
        )

    user_front_settings_1_3 = await CrudUserFrontSettings.get_row_by_user_id(user_1.id)
    assert user_front_settings_1_3.gallery_preview_size is None
    assert user_front_settings_1_3.gallery_image_auto_play_time_interval is None
    assert user_front_settings_1_3.gallery_image_preview_size is None
    assert user_front_settings_1_3.video_preview_size is None
