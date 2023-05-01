from back.utils.dt import iso2datetime
from sqlalchemy import TIMESTAMP, VARCHAR, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from ...base import Base


class UserElasticCountQuestBase(Base):
    __tablename__ = "user_elastic_count_quest"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(64), nullable=False)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    numerator_id = Column(
        Integer,
        ForeignKey("user_elastic_count_query.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    denominator_id = Column(
        Integer,
        ForeignKey("user_elastic_count_query.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created = Column(TIMESTAMP, server_default=func.now())
    modified = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "numerator_id",
            "denominator_id",
            name="uc_user_elastic_count_quest",
        ),
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
