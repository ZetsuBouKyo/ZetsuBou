from sqlalchemy import TEXT, TIMESTAMP, VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from back.utils.dt import iso2datetime

from ...base import Base


class UserElasticCountQueryBase(Base):
    __tablename__ = "user_elastic_count_query"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name = Column(VARCHAR(64), nullable=False)
    query = Column(TEXT)
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
