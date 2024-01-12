from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from back.utils.dt import iso2datetime

from ...base import Base


class UserBookmarkVideoBase(Base):
    __tablename__ = "user_bookmark_video"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )

    video_id = Column(VARCHAR(64), nullable=False)
    time = Column(Integer, nullable=False)

    modified = Column(TIMESTAMP, server_default=func.now())

    @validates("modified")
    def validate_modified(self, _, value):
        return iso2datetime(value)
