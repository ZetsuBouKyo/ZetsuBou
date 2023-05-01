from ....base import Base
from ..mixin import SettingFrontTokenMixin


class SettingFrontGalleryTagFieldBase(Base, SettingFrontTokenMixin):
    __tablename__: str = "setting_front_gallery_tag_field"
