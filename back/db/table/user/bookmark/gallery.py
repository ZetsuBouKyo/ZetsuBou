from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from back.utils.dt import iso2datetime

from ...base import Base


class UserBookmarkGalleryBase(Base):
    __tablename__ = "user_bookmark_gallery"
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )

    gallery_id = Column(VARCHAR(64), nullable=False)
    page = Column(Integer, nullable=False)

    modified = Column(TIMESTAMP, server_default=func.now())

    @validates("modified")
    def validate_modified(self, _, value):
        if type(value) is str:
            return iso2datetime(value)
        return value
