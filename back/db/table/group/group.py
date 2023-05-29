from sqlalchemy import VARCHAR, Column, Integer
from sqlalchemy.orm import validates

from ..base import Base


class GroupBase(Base):
    __tablename__ = "group"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(64), nullable=False, unique=True)

    @validates("name")
    def validate_name(self, _, name):
        return name.lower()
