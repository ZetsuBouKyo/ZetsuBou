from sqlalchemy import TEXT, VARCHAR, Column, Integer, UniqueConstraint

from ..base import Base


class StorageMinioBase(Base):
    __tablename__: str = "storage_minio"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(Integer, index=True, nullable=False)
    name = Column(VARCHAR(32), nullable=False)
    endpoint = Column(TEXT, nullable=False)
    bucket_name = Column(VARCHAR(63), nullable=False)
    prefix = Column(VARCHAR(1024), nullable=False)
    depth = Column(Integer, nullable=False)
    access_key = Column(VARCHAR(128), nullable=False)
    secret_key = Column(VARCHAR(128), nullable=False)

    __table_args__ = (
        UniqueConstraint("endpoint", "bucket_name", "prefix", name="uc_storage_minio"),
    )
