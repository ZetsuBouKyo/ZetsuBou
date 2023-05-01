from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from .base import Base


class ScopeBase(Base):
    __tablename__: str = "scope"
    p_id = Column(Integer, primary_key=True)
    id = Column(Integer, nullable=False, index=True)
    group_id = Column(
        Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False, index=True
    )
    __table_args__ = (UniqueConstraint("id", "group_id", name="uc_scope_id_group_id"),)
