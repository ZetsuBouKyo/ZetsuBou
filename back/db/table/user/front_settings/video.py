from sqlalchemy import Column, Integer

from ...base import Base
from .mixin import UserFrontSettingsMixin


class UserFrontSettingsVideoPreviewSize(Base, UserFrontSettingsMixin):
    __tablename__: str = "user_front_settings_video_ps"

    size: int = Column(Integer, nullable=False)
