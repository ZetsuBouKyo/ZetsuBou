import pytest

from back.model.base import SourceBaseModel, SourceProtocolEnum
from tests.general.logger import logger


def get_path(
    protocol: SourceProtocolEnum, storage_id: int, bucket_name: str, object_name: str
):
    return f"{protocol}-{storage_id}://{bucket_name}{object_name}"


def test_1():
    data = [
        (SourceProtocolEnum.MINIO.value, 1, "test", "/"),
        (SourceProtocolEnum.MINIO.value, 1, "test", "/abc/def"),
        (SourceProtocolEnum.MINIO.value, 1, "test", "/abc/def/"),
    ]
    for d in data:
        path = get_path(*d)
        logger.info(f"path: {path}")
        source = SourceBaseModel(path=path)
        assert source.protocol == d[0]
        assert source.storage_id == d[1]
        assert source.bucket_name == d[2]
        assert source.object_name == d[3]


def test_type_error():
    protocol = SourceProtocolEnum.MINIO.value
    storage_id = "abc"
    bucket_name = "test"
    object_name = "/abc/def/"
    path = get_path(protocol, storage_id, bucket_name, object_name)
    logger.info(f"path: {path}")

    with pytest.raises(ValueError):
        source = SourceBaseModel(path=path)
        source.storage_id


def test_none():
    path = ""
    logger.info(f"path: {path}")
    source = SourceBaseModel(path=path)

    assert source.protocol is None
    assert source.storage_id is None
    assert source.bucket_name is None
    assert source.object_name is None
