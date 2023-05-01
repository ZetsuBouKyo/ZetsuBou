from ....base import Base
from ..mixin import SettingFrontTokenMixin


class SettingFrontGalleryCategoryBase(Base, SettingFrontTokenMixin):
    __tablename__: str = "setting_front_gallery_category"
