from sqlalchemy import Column, Integer

from ...base import Base
from .mixin import UserFrontSettingsMixin


class UserFrontSettingsGalleryPreviewSizeBase(Base, UserFrontSettingsMixin):
    __tablename__: str = "user_front_settings_gallery_ps"

    size: int = Column(Integer, nullable=False)


class UserFrontSettingsGalleryImagePreviewSizeBase(Base, UserFrontSettingsMixin):
    __tablename__: str = "user_front_settings_gallery_ips"

    size: int = Column(Integer, nullable=False)


class UserFrontSettingsGalleryImageAutoPlayTimeIntervalBase(
    Base, UserFrontSettingsMixin
):
    __tablename__: str = "user_front_settings_gallery_iapti"

    interval: int = Column(Integer, nullable=False)
