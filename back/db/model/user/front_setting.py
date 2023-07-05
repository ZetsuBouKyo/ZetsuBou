from pydantic import BaseModel

from back.utils.model import DatetimeStr


class UserFrontSettingCreate(BaseModel):
    user_id: int
    gallery_preview_size: int
    video_preview_size: int
    img_preview_size: int
    auto_play_time_interval: int


class UserFrontSettingCreated(BaseModel):
    id: int
    user_id: int
    gallery_preview_size: int
    video_preview_size: int
    img_preview_size: int
    auto_play_time_interval: int


class UserFrontSettingUpdateByUserId(BaseModel):
    user_id: int
    gallery_preview_size: int
    video_preview_size: int
    img_preview_size: int
    auto_play_time_interval: int


class UserFrontSetting(BaseModel):
    id: int
    user_id: int
    gallery_preview_size: int
    video_preview_size: int
    img_preview_size: int
    auto_play_time_interval: int
    created: DatetimeStr
    modified: DatetimeStr
