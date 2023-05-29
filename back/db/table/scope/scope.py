from sqlalchemy import VARCHAR, Column, Integer

from ..base import Base


class ScopeBase(Base):
    __tablename__: str = "scope"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(256), nullable=False, index=True, unique=True)
