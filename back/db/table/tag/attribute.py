from sqlalchemy import VARCHAR, Column, Integer
from sqlalchemy.orm import validates

from ..base import Base


class TagAttributeBase(Base):
    __tablename__: str = "tag_attribute"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(32), nullable=False, index=True, unique=True)

    @validates("name")
    def validate_name(self, _, name):
        return name.lower()
