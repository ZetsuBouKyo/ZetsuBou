from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr


class SettingFrontTokenMixin:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def token_id(cls):
        return Column(
            Integer,
            ForeignKey("tag_token.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
            unique=True,
        )

    enable = Column(Boolean, nullable=False)
