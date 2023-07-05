from sqlalchemy import TIMESTAMP, VARCHAR, Column, Integer
from sqlalchemy.orm import validates
from sqlalchemy.sql import functions as func

from back.utils.dt import iso2datetime

from ..base import Base


class UserBase(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(64), nullable=False)
    email = Column(VARCHAR(254), nullable=False, unique=True)
    hashed_password = Column(VARCHAR(128), nullable=False)
    created = Column(TIMESTAMP, server_default=func.now())
    last_signin = Column(TIMESTAMP, server_default=func.now())

    @validates("created")
    def validate_created(self, _, value):
        if type(value) is str:
            return iso2datetime(value)
        return value

    @validates("last_signin")
    def validate_last_signin(self, _, value):
        if type(value) is str:
            return iso2datetime(value)
        return value
