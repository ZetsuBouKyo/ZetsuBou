from __future__ import annotations

from enum import Enum
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, PositiveInt


class SourceProtocolEnum(str, Enum):
    MINIO: str = "minio"


class Pagination(BaseModel):
    page: PositiveInt = 1
    size: PositiveInt = 20
    is_desc: bool = False

    @property
    def skip(cls):
        return (cls.page - 1) * cls.size


class SourceBaseModel(BaseModel):
    # To allow the `Source' class to initialise with an empty dictionary object, we need
    # a default value for the `path' parameter.
    path: Optional[str] = Field(
        default=None,
        title="Path",
        description="File path with custom protocol.",
        examples=["minio-1://bucket/prefix_1/prefix_1_1"],
    )

    @property
    def _url(cls):
        return urlparse(cls.path)

    @property
    def _scheme(cls):
        return cls._url.scheme

    @property
    def protocol(cls):
        if cls.path is None:
            return None

        if cls._scheme.startswith(SourceProtocolEnum.MINIO.value):
            return SourceProtocolEnum.MINIO.value
        return None

    @property
    def bucket_name(cls):
        if cls.path is None:
            return None

        if cls.protocol == SourceProtocolEnum.MINIO.value:
            return cls._url.netloc
        return None

    @property
    def object_name(cls):
        if cls.path is None:
            return None

        if cls.protocol == SourceProtocolEnum.MINIO.value:
            return cls._url.path
        return None

    @property
    def storage_id(cls) -> int:
        if cls.path is None:
            return None

        if cls.protocol == SourceProtocolEnum.MINIO.value:
            if cls._scheme[5] == "-":
                id = cls._scheme[len(SourceProtocolEnum.MINIO.value) + 1 :]
                return int(id)
        return None

    def get_joined_source(cls, *paths: str) -> SourceBaseModel:
        _base_path = cls.path
        if _base_path is None:
            raise ValueError(f"`path` value should not be None.")

        _paths = []
        for path in paths:
            _path = path
            if _path.startswith("/"):
                _path = _path[1:]
            if _path.endswith("/"):
                _path = _path[:-1]
            _paths.append(_path)
        _relative_path = "/".join(_paths)

        if _base_path.endswith("/"):
            _new_path = f"{_base_path}{_relative_path}"
        else:
            _new_path = f"{_base_path}/{_relative_path}"

        if paths[-1].endswith("/") and not _new_path.endswith("/"):
            _new_path += "/"

        return SourceBaseModel(path=_new_path)
