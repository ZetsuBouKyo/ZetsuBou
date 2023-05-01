from sqlalchemy import VARCHAR, Column, Float, Integer

from .base import Base


class ImageBase(Base):
    __tablename__: str = "image"
    id = Column(Integer, primary_key=True, index=True)
    gallery_id = Column(VARCHAR(36), unique=True)
    width = Column(Integer)
    height = Column(Integer)
    slope = Column(Float)
    fname = Column(VARCHAR(255))
    md5 = Column(VARCHAR(32))
