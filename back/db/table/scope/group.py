from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from ..base import Base


class ScopeGroupBase(Base):
    __tablename__: str = "scope_group"
    id = Column(Integer, primary_key=True)
    scope_id = Column(
        Integer, ForeignKey("scope.id", ondelete="CASCADE"), nullable=False, index=True
    )
    group_id = Column(
        Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False, index=True
    )
    __table_args__ = (
        UniqueConstraint("scope_id", "group_id", name="uc_scope_id_group_id"),
    )
