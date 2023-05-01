from ....base import Base
from ..mixin import SettingFrontTokenMixin


class SettingFrontVideoCategoryBase(Base, SettingFrontTokenMixin):
    __tablename__: str = "setting_front_video_category"
