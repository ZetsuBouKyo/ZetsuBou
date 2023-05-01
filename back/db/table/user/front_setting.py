from back.utils.dt import iso2datetime
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from ..base import Base


class UserFrontSettingBase(Base):
    __tablename__ = "user_front_setting"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    gallery_preview_size = Column(Integer)
    video_preview_size = Column(Integer)
    img_preview_size = Column(Integer)
    auto_play_time_interval = Column(Integer)
    created = Column(TIMESTAMP, server_default=func.now())
    modified = Column(TIMESTAMP, server_default=func.now())

    @validates("created")
    def validate_created(self, _, value):
        if type(value) is str:
            return iso2datetime(value)
        return value

    @validates("modified")
    def validate_modified(self, _, value):
        if type(value) is str:
            return iso2datetime(value)
        return value
