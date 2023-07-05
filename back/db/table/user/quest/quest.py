from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    Column,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from back.utils.dt import iso2datetime

from ...base import Base


class UserQuestBase(Base):
    __tablename__ = "user_quest"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = Column(VARCHAR(64), nullable=False)
    category_id = Column(
        Integer,
        ForeignKey("user_quest_category.id", ondelete="CASCADE"),
        nullable=False,
    )
    quest_id = Column(Integer, nullable=False)
    priority = Column(Integer, nullable=False, unique=True)
    created = Column(TIMESTAMP, server_default=func.now())
    modified = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "category_id", "quest_id", name="uc_user_quest"),
    )

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


Index("ix_user_quest_c_category_id", UserQuestBase.category_id)
