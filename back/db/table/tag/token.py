from sqlalchemy import VARCHAR, Column, Integer

from ..base import Base


class TagTokenBase(Base):
    __tablename__: str = "tag_token"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(256), nullable=False, index=True)
