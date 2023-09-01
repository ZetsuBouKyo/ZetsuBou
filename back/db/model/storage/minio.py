from typing import Optional

from pydantic import BaseModel

from back.model.storage import StorageCategoryEnum


class StorageMinioCreate(BaseModel):
    category: StorageCategoryEnum
    name: Optional[str] = None
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str

    class Config:
        use_enum_values = True


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
    id: int
    category: StorageCategoryEnum
    name: str
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str

    class Config:
        use_enum_values = True


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
