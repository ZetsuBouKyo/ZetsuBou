from sqlalchemy import VARCHAR, Column, Integer

from ...base import Base


class UserQuestCategoryBase(Base):
    __tablename__ = "user_quest_category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(VARCHAR(64), nullable=False, unique=True)
