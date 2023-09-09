from typing import Optional

from pydantic import BaseModel


class UserFrontSettingsCreate(BaseModel):
    user_id: int
    gallery_preview_size: int
    gallery_image_auto_play_time_interval: int
    gallery_image_preview_size: int
    video_preview_size: int


UserFrontSettingsCreated = UserFrontSettingsCreate


class UserFrontSettingsUpdateByUserId(BaseModel):
    user_id: int
    gallery_preview_size: Optional[int] = None
    gallery_image_auto_play_time_interval: Optional[int] = None
    gallery_image_preview_size: Optional[int] = None
    video_preview_size: Optional[int] = None


class UserFrontSettings(BaseModel):
    user_id: int
    gallery_preview_size: Optional[int]
    gallery_image_auto_play_time_interval: Optional[int]
    gallery_image_preview_size: Optional[int]
    video_preview_size: Optional[int]
