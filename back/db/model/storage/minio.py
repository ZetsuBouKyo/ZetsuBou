from typing import Optional

from pydantic import BaseModel, ConfigDict

from back.model.storage import StorageCategoryEnum
from back.utils.model import HttpUrlStr


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


StorageMinio = StorageMinioUpdate = StorageMinioCreated
