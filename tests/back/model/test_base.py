from typing import Union

import pytest

from back.model.base import SourceBaseModel, SourceProtocolEnum
from tests.general.logging import logger
from tests.general.summary import print_divider


def get_path(
    protocol: SourceProtocolEnum,
    storage_id: Union[int, str],
    bucket_name: str,
    object_name: str,
):
    return f"{protocol}-{storage_id}://{bucket_name}{object_name}"


def test_source_base_model():
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
        print_divider()


def test_source_base_model_get_joined_source():
    path = get_path(SourceProtocolEnum.MINIO.value, 1, "test", "/")
    logger.info(f"base path: {path}")

    source = SourceBaseModel(path=path)

    data = [
        (("/"), "minio-1://test/"),
        (("abc", "def"), "minio-1://test/abc/def"),
        (("abc", "def/"), "minio-1://test/abc/def/"),
        (("/abc/", "/def/"), "minio-1://test/abc/def/"),
    ]

    for d in data:
        paths, ans = d[0], d[1]
        new_path = source.get_joined_source(*paths)
        logger.info(f"new path: {new_path}")
        logger.info(f"ans: {ans}")

        assert new_path.path == ans
        print_divider()


def test_source_base_model_get_joined_source_without_slash():
    path = get_path(SourceProtocolEnum.MINIO.value, 1, "test", "")
    logger.info(f"base path: {path}")

    source = SourceBaseModel(path=path)

    data = [
        (("/"), "minio-1://test/"),
        (("abc", "def"), "minio-1://test/abc/def"),
        (("abc", "def/"), "minio-1://test/abc/def/"),
        (("/abc/", "/def/"), "minio-1://test/abc/def/"),
    ]

    for d in data:
        paths, ans = d[0], d[1]
        new_path = source.get_joined_source(*paths)
        logger.info(f"new path: {new_path}")
        logger.info(f"ans: {ans}")

        assert new_path.path == ans
        print_divider()


def test_source_base_model_type_error():
    protocol = SourceProtocolEnum.MINIO.value
    storage_id = "abc"
    bucket_name = "test"
    object_name = "/abc/def/"
    path = get_path(protocol, storage_id, bucket_name, object_name)
    logger.info(f"path: {path}")

    with pytest.raises(ValueError):
        source = SourceBaseModel(path=path)
        source.storage_id


def test_source_base_model_empty():
    path = ""
    logger.info(f"path: {path}")
    source = SourceBaseModel(path=path)

    assert source.protocol is None
    assert source.storage_id is None
    assert source.bucket_name is None
    assert source.object_name is None


def test_source_base_model_none():
    path = None
    logger.info(f"path: {path}")
    source = SourceBaseModel(path=path)

    assert source.protocol is None
    assert source.storage_id is None
    assert source.bucket_name is None
    assert source.object_name is None

    with pytest.raises(ValueError):
        source.get_joined_source("")
