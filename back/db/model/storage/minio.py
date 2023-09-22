from typing import Optional

from pydantic import BaseModel, ConfigDict

from back.model.storage import StorageCategoryEnum


class StorageMinioCreate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    category: StorageCategoryEnum
    name: Optional[str] = None
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str


class StorageMinioCreated(BaseModel):
    id: int
    category: StorageCategoryEnum
    name: Optional[str] = None
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str


class StorageMinioUpdate(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: int
    category: StorageCategoryEnum
    name: str
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str


class StorageMinio(BaseModel):
    id: int
    category: StorageCategoryEnum
    name: str
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str
