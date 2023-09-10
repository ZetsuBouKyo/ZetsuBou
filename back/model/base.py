from enum import Enum
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field


class SourceProtocolEnum(str, Enum):
    MINIO: str = "minio"


class Pagination(BaseModel):
    page: int = 1
    size: int = 20
    is_desc: bool = False

    @property
    def skip(cls):
        return (cls.page - 1) * cls.size


class SourceBaseModel(BaseModel):
    path: Optional[str] = Field(
        default=None,
        title="Path",
        description="File path with custom protocol.",
        example="minio-1://bucket/prefix_1/prefix_1_1",
    )

    @property
    def _url(cls):
        return urlparse(cls.path)

    @property
    def _scheme(cls):
        return cls._url.scheme

    @property
    def protocol(cls):
        if cls._scheme.startswith(SourceProtocolEnum.MINIO.value):
            return SourceProtocolEnum.MINIO.value
        return None

    @property
    def bucket_name(cls):
        if cls.protocol == SourceProtocolEnum.MINIO.value:
            return cls._url.netloc
        return None

    @property
    def object_name(cls):
        if cls.protocol == SourceProtocolEnum.MINIO.value:
            return cls._url.path
        return None

    @property
    def storage_id(cls) -> int:
        if cls.protocol == SourceProtocolEnum.MINIO.value:
            try:
                if cls._scheme[5] == "-":
                    id = cls._scheme[len(SourceProtocolEnum.MINIO.value) + 1 :]
                    return int(id)
            except IndexError:
                return None
        return None
