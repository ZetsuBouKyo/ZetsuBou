import pytest

from back.db.crud import CrudStorageMinio
from back.db.model import StorageMinioCreate, StorageMinioUpdate
from back.model.storage import StorageCategoryEnum
from lib.faker import ZetsuBouFaker
from tests.general.session import DatabaseSession


@pytest.mark.asyncio
@pytest.mark.integration
async def test_crud_gallery():
    async with DatabaseSession():
        faker = ZetsuBouFaker()

        storage_total_0 = await CrudStorageMinio.count_total()

        # create MinIO storage
        storage_category_1 = StorageCategoryEnum.gallery
        storage_name_1 = faker.name()
        storage_endpoint_1 = faker.url()
        storage_bucket_name_1 = faker.random_string(10)
        storage_prefix_1 = f"{faker.name()}/"
        storage_depth_1 = 1
        storage_access_key_1 = faker.random_string(10)
        storage_secret_key_1 = faker.random_string(16)

        storage_1 = StorageMinioCreate(
            category=storage_category_1,
            name=storage_name_1,
            endpoint=storage_endpoint_1,
            bucket_name=storage_bucket_name_1,
            prefix=storage_prefix_1,
            depth=storage_depth_1,
            access_key=storage_access_key_1,
            secret_key=storage_secret_key_1,
        )

        storage_1_created = await CrudStorageMinio.create(storage_1)

        # test `safe_create`
        storages_1_0 = await CrudStorageMinio.get_all_rows_by_name_order_by_id(
            storage_name_1
        )

        storage_1_safe_created = await CrudStorageMinio.safe_create(storage_1)
        assert storage_1.category == storage_1_safe_created.category
        assert storage_1.name == storage_1_safe_created.name
        assert storage_1.endpoint == storage_1_safe_created.endpoint
        assert storage_1.bucket_name == storage_1_safe_created.bucket_name
        assert storage_1.prefix == storage_1_safe_created.prefix
        assert storage_1.depth == storage_1_safe_created.depth
        assert storage_1.access_key == storage_1_safe_created.access_key
        assert storage_1.secret_key == storage_1_safe_created.secret_key

        storages_1_1 = await CrudStorageMinio.get_all_rows_by_name_order_by_id(
            storage_name_1
        )

        assert len(storages_1_0) == len(storages_1_1)

        # test
        storage_1_by_id = await CrudStorageMinio.get_row_by_id(storage_1_created.id)
        assert storage_1_by_id is not None

        storage_total_1 = await CrudStorageMinio.count_total()
        assert storage_total_1 == storage_total_0 + 1

        storages = await CrudStorageMinio.get_rows_order_by_id()
        assert len(storages) > 0

        # create MinIO storage
        storage_category_2 = StorageCategoryEnum.gallery
        storage_name_2 = faker.name()
        storage_endpoint_2 = faker.url()
        storage_bucket_name_2 = faker.random_string(10)
        storage_prefix_2 = f"{faker.name()}/"
        storage_depth_2 = 1
        storage_access_key_2 = faker.random_string(10)
        storage_secret_key_2 = faker.random_string(16)

        storage_2 = StorageMinioCreate(
            category=storage_category_2,
            name=storage_name_2,
            endpoint=storage_endpoint_2,
            bucket_name=storage_bucket_name_2,
            prefix=storage_prefix_2,
            depth=storage_depth_2,
            access_key=storage_access_key_2,
            secret_key=storage_secret_key_2,
        )

        storage_2_created = await CrudStorageMinio.create(storage_2)

        # update the storage
        storage_name_2_to_update = faker.name()
        storage_2_to_update = StorageMinioUpdate(
            id=storage_2_created.id,
            category=storage_category_2,
            name=storage_name_2_to_update,
            endpoint=storage_endpoint_2,
            bucket_name=storage_bucket_name_2,
            prefix=storage_prefix_2,
            depth=storage_depth_2,
            access_key=storage_access_key_2,
            secret_key=storage_secret_key_2,
        )
        await CrudStorageMinio.update_by_id(storage_2_to_update)
        storage_2_updated = await CrudStorageMinio.get_row_by_id(storage_2_created.id)
        assert storage_2_updated.id == storage_2_created.id
        assert storage_2_updated.name == storage_name_2_to_update

        # test
        count = 0
        async for _ in CrudStorageMinio.iter_order_by_id(limit=1):
            count += 1
        total = await CrudStorageMinio.count_total()

        has_value = False
        async for row in CrudStorageMinio.iter_by_category_order_by_id(
            StorageCategoryEnum.gallery
        ):
            has_value = True
            assert row.category == StorageCategoryEnum.gallery
        assert has_value

        assert count == total

        # safe create MinIO storage
        storage_category_3 = StorageCategoryEnum.gallery
        storage_name_3 = storage_name_1
        storage_endpoint_3 = faker.url()
        storage_bucket_name_3 = faker.random_string(10)
        storage_prefix_3 = f"{faker.name()}/"
        storage_depth_3 = 1
        storage_access_key_3 = faker.random_string(10)
        storage_secret_key_3 = faker.random_string(16)

        storage_3 = StorageMinioCreate(
            category=storage_category_3,
            name=storage_name_3,
            endpoint=storage_endpoint_3,
            bucket_name=storage_bucket_name_3,
            prefix=storage_prefix_3,
            depth=storage_depth_3,
            access_key=storage_access_key_3,
            secret_key=storage_secret_key_3,
        )

        storages_3_0 = await CrudStorageMinio.get_all_rows_by_name_order_by_id(
            storage_name_3
        )

        storage_3_created = await CrudStorageMinio.safe_create(storage_3)

        storages_3_1 = await CrudStorageMinio.get_all_rows_by_name_order_by_id(
            storage_name_3
        )

        assert len(storages_3_0) + 1 == len(storages_3_1)

        # delete
        await CrudStorageMinio.delete_by_id(storage_1_created.id)
        storage_1_deleted = await CrudStorageMinio.get_row_by_id(storage_1_created.id)
        assert storage_1_deleted is None

        await CrudStorageMinio.delete_by_id(storage_2_created.id)
        storage_2_deleted = await CrudStorageMinio.get_row_by_id(storage_2_created.id)
        assert storage_2_deleted is None

        await CrudStorageMinio.delete_by_id(storage_3_created.id)
        storage_3_deleted = await CrudStorageMinio.get_row_by_id(storage_3_created.id)
        assert storage_3_deleted is None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_crud_video():
    async with DatabaseSession():
        faker = ZetsuBouFaker()

        storage_total_0 = await CrudStorageMinio.count_total()

        # create MinIO storage
        storage_category_1 = StorageCategoryEnum.video
        storage_name_1 = faker.name()
        storage_endpoint_1 = faker.url()
        storage_bucket_name_1 = faker.random_string(10)
        storage_prefix_1 = f"{faker.name()}/"
        storage_depth_1 = 1
        storage_access_key_1 = faker.random_string(10)
        storage_secret_key_1 = faker.random_string(16)

        storage_1 = StorageMinioCreate(
            category=storage_category_1,
            name=storage_name_1,
            endpoint=storage_endpoint_1,
            bucket_name=storage_bucket_name_1,
            prefix=storage_prefix_1,
            depth=storage_depth_1,
            access_key=storage_access_key_1,
            secret_key=storage_secret_key_1,
        )

        with pytest.raises(AssertionError):
            await CrudStorageMinio.create(storage_1)

        storage_total_1 = await CrudStorageMinio.count_total()
        assert storage_total_0 == storage_total_1

        storage_1.depth = -1
        storage_1_created = await CrudStorageMinio.create(storage_1)

        await CrudStorageMinio.delete_by_id(storage_1_created.id)
        storage_1_deleted = await CrudStorageMinio.get_row_by_id(storage_1_created.id)
        assert storage_1_deleted is None
