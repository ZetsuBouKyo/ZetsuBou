from typing import Optional

from pydantic import BaseModel, ConfigDict

from back.model.base import SourceBaseModel, SourceProtocolEnum
from back.model.storage import StorageCategoryEnum
from back.model.string import HttpUrlStr


class StorageMinioCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    category: StorageCategoryEnum
    name: str
    endpoint: HttpUrlStr
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str


class StorageMinioCreated(StorageMinioCreate):
    id: int

    @property
    def path(cls) -> str:
        if hasattr(cls, "_path"):
            return cls._path
        cls._path = f"{SourceProtocolEnum.MINIO.value}-{cls.id}://{cls.bucket_name}/{cls.prefix}"
        return cls._path

    @property
    def source(cls) -> SourceBaseModel:
        return SourceBaseModel(path=cls.path)


StorageMinio = StorageMinioUpdate = StorageMinioCreated
