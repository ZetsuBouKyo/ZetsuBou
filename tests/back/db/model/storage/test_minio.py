from back.db.model import StorageMinio
from back.model.base import SourceProtocolEnum
from back.model.storage import StorageCategoryEnum
from lib.faker import ZetsuBouFaker
from tests.general.logger import logger
from tests.general.summary import print_divider


def test_right_data():
    faker = ZetsuBouFaker()
    right_data = [
        {
            "id": 1,
            "category": StorageCategoryEnum.gallery,
            "name": faker.name(),
            "endpoint": faker.url(),
            "bucket_name": faker.random_string(10),
            "prefix": f"{faker.name()}/",
            "depth": 1,
            "access_key": faker.random_string(10),
            "secret_key": faker.random_string(16),
        },
        {
            "id": 1,
            "category": StorageCategoryEnum.gallery.value,
            "name": faker.name(),
            "endpoint": faker.url(),
            "bucket_name": faker.random_string(10),
            "prefix": f"{faker.name()}/",
            "depth": 2,
            "access_key": faker.random_string(10),
            "secret_key": faker.random_string(16),
        },
        {
            "id": 1,
            "category": StorageCategoryEnum.video,
            "name": faker.name(),
            "endpoint": faker.url(),
            "bucket_name": faker.random_string(10),
            "prefix": f"{faker.name()}/{faker.name()}/",
            "depth": -1,
            "access_key": faker.random_string(10),
            "secret_key": faker.random_string(16),
        },
        {
            "id": 1,
            "category": StorageCategoryEnum.video,
            "name": faker.name(),
            "endpoint": faker.url(),
            "bucket_name": faker.random_string(10),
            "prefix": "",
            "depth": -1,
            "access_key": faker.random_string(10),
            "secret_key": faker.random_string(16),
        },
    ]

    for data in right_data:
        for key, value in data.items():
            logger.info(f"{key}: {value}")
        storage = StorageMinio(**data)
        id = data.get("id")
        bucket_name = data.get("bucket_name")
        prefix = data.get("prefix")
        path = f"{SourceProtocolEnum.MINIO.value}-{id}://{bucket_name}/{prefix}"
        logger.info(f"path: {path}")

        assert not storage.path.endswith("//")
        assert storage.path.endswith("/")
        assert storage.path == path
        assert storage.source.path == path
        print_divider()
