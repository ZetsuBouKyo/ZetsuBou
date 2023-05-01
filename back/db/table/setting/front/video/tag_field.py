from ....base import Base
from ..mixin import SettingFrontTokenMixin


class SettingFrontVideoTagFieldBase(Base, SettingFrontTokenMixin):
    __tablename__: str = "setting_front_video_tag_field"
