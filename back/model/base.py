from enum import Enum
from urllib.parse import urlparse

from pydantic import BaseModel


class Protocol(str, Enum):
    MINIO: str = "minio"


class Pagination(BaseModel):
    page: int = 1
    size: int = 20
    is_desc: bool = False

    @property
    def skip(cls):
        return (cls.page - 1) * cls.size


class SourceBaseModel(BaseModel):
    path: str

    @property
    def _url(cls):
        return urlparse(cls.path)

    @property
    def _scheme(cls):
        return cls._url.scheme

    @property
    def protocol(cls):
        if cls._scheme.startswith(Protocol.MINIO.value):
            return Protocol.MINIO.value
        return None

    @property
    def bucket_name(cls):
        if cls.protocol == Protocol.MINIO.value:
            return cls._url.netloc
        return None

    @property
    def object_name(cls):
        if cls.protocol == Protocol.MINIO.value:
            return cls._url.path
        return None

    # TODO: deprecated
    @property
    def minio_storage_id(cls) -> int:
        if cls.protocol == Protocol.MINIO.value:
            if cls._scheme[5] == "-":
                id = cls._scheme[len(Protocol.MINIO.value) + 1 :]
            return int(id)
        return None

    @property
    def storage_minio_id(cls) -> int:
        if cls.protocol == Protocol.MINIO.value:
            if cls._scheme[5] == "-":
                id = cls._scheme[len(Protocol.MINIO.value) + 1 :]
                return int(id)
        return None
