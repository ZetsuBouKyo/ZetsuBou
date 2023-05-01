from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, UniqueConstraint

from ..base import Base


class TagSynonymBase(Base):
    __tablename__: str = "tag_synonym"
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
        UniqueConstraint("linked_id", "token_id", name="uc_tag_synonym"),
        CheckConstraint("linked_id != token_id"),
    )
