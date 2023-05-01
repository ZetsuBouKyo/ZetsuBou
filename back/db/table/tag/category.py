from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, UniqueConstraint

from ..base import Base


class TagCategoryBase(Base):
    __tablename__: str = "tag_category"
    id = Column(Integer, primary_key=True, index=True)
    linked_id = Column(
        Integer,
        ForeignKey("tag_token.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    token_id = Column(
        Integer,
        ForeignKey("tag_token.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    __table_args__ = (
        UniqueConstraint("linked_id", "token_id", name="uc_tag_category"),
        CheckConstraint("linked_id != token_id"),
    )
