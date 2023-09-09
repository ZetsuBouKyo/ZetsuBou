from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.ext.declarative import declared_attr


class UserFrontSettingsMixin:
    id = Column(Integer, primary_key=True, index=True)

    @declared_attr
    def user_id(cls):
        return Column(
            Integer,
            ForeignKey("user.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
            unique=True,
        )
