from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint

from ..base import Base


class UserGroupBase(Base):
    __tablename__ = "user_group"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    group_id = Column(
        Integer, ForeignKey("group.id", ondelete="CASCADE"), nullable=False, index=True
    )
    __table_args__ = (UniqueConstraint("user_id", "group_id", name="uc_user_group"),)
