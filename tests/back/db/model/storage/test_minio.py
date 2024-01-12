from back.db.model import StorageMinio
from back.model.storage import StorageCategoryEnum
from lib.faker import ZetsuBouFaker
from tests.general.logger import logger


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
            "category": StorageCategoryEnum.gallery,
            "name": faker.name(),
            "endpoint": faker.url(),
            "bucket_name": faker.random_string(10),
            "prefix": f"{faker.name()}/{faker.name()}/",
            "depth": 1,
            "access_key": faker.random_string(10),
            "secret_key": faker.random_string(16),
        },
    ]

    for data in right_data:
        for key, value in data.items():
            logger.info(f"{key}: {value}")
        StorageMinio(**data)
