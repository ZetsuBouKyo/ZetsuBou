from back.model.base import SourceBaseModel, SourceProtocolEnum


def assert_source_base_model(
    protocol: SourceProtocolEnum, storage_id: int, bucket_name: str, object_name: str
):
    path = f"{protocol}-{storage_id}://{bucket_name}{object_name}"
    source = SourceBaseModel(path=path)

    assert source.protocol == protocol
    assert source.storage_id == storage_id
    assert source.bucket_name == bucket_name
    assert source.object_name == object_name


def test_1():
    protocol = SourceProtocolEnum.MINIO.value
    storage_id = 1
    bucket_name = "test"
    object_name = "/"

    assert_source_base_model(protocol, storage_id, bucket_name, object_name)


def test_2():
    protocol = SourceProtocolEnum.MINIO.value
    storage_id = 1
    bucket_name = "test"
    object_name = "/abc/def"

    assert_source_base_model(protocol, storage_id, bucket_name, object_name)


def test_3():
    protocol = SourceProtocolEnum.MINIO.value
    storage_id = 1
    bucket_name = "test"
    object_name = "/abc/def/"

    assert_source_base_model(protocol, storage_id, bucket_name, object_name)
