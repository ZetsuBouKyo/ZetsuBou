from enum import Enum

from pydantic import BaseModel


class MinioStorageCategoryEnum(int, Enum):
    gallery: int = 0
    video: int = 1


class MinioStorageCreate(BaseModel):
    category: MinioStorageCategoryEnum
    name: str = None
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str

    class Config:
        use_enum_values = True


class MinioStorageCreated(BaseModel):
    id: int
    category: MinioStorageCategoryEnum
    name: str = None
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str


class MinioStorageUpdate(BaseModel):
    id: int
    category: MinioStorageCategoryEnum
    name: str
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str

    class Config:
        use_enum_values = True


class MinioStorage(BaseModel):
    id: int
    category: MinioStorageCategoryEnum
    name: str
    endpoint: str
    bucket_name: str
    prefix: str
    depth: int
    access_key: str
    secret_key: str
