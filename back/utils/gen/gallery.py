import io
from typing import Awaitable, Callable, Tuple

from PIL import Image

from back.db.crud import CrudStorageMinio
from back.db.model import StorageMinio, StorageMinioCreate
from back.model.gallery import Gallery
from back.model.storage import StorageCategoryEnum
from back.session.storage import get_storage_session_by_source
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from lib.faker import ZetsuBouFaker

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname

STORAGE_S3_ENDPOINT_URL = setting.storage_s3_endpoint_url
STORAGE_S3_AWS_ACCESS_KEY_ID = setting.storage_s3_aws_access_key_id
STORAGE_S3_AWS_SECRET_ACCESS_KEY = setting.storage_s3_aws_secret_access_key

STORAGE_CACHE = setting.storage_cache
STORAGE_TESTS = setting.storage_tests
STORAGE_TESTS_GALLERIES = setting.storage_tests_galleries

delete_gallery_prefix = f"{STORAGE_TESTS}/{STORAGE_TESTS_GALLERIES}/delete/"
delete_gallery_storage_name = "tests delete galleries"
delete_gallery_storage = StorageMinioCreate(
    category=StorageCategoryEnum.gallery,
    name=delete_gallery_storage_name,
    endpoint=STORAGE_S3_ENDPOINT_URL,
    bucket_name=STORAGE_CACHE,
    prefix=delete_gallery_prefix,
    depth=1,
    access_key=STORAGE_S3_AWS_ACCESS_KEY_ID,
    secret_key=STORAGE_S3_AWS_SECRET_ACCESS_KEY,
)

simple_gallery_prefix = f"{STORAGE_TESTS}/{STORAGE_TESTS_GALLERIES}/simple/"
simple_gallery_storage_name = "tests simple galleries"
simple_gallery_storage = StorageMinioCreate(
    category=StorageCategoryEnum.gallery,
    name=simple_gallery_storage_name,
    endpoint=STORAGE_S3_ENDPOINT_URL,
    bucket_name=STORAGE_CACHE,
    prefix=simple_gallery_prefix,
    depth=1,
    access_key=STORAGE_S3_AWS_ACCESS_KEY_ID,
    secret_key=STORAGE_S3_AWS_SECRET_ACCESS_KEY,
)

nested_gallery_prefix = f"{STORAGE_TESTS}/{STORAGE_TESTS_GALLERIES}/nested/"
nested_gallery_storage_name = "tests nested galleries"
nested_gallery_storage = StorageMinioCreate(
    category=StorageCategoryEnum.gallery,
    name=nested_gallery_storage_name,
    endpoint=STORAGE_S3_ENDPOINT_URL,
    bucket_name=STORAGE_CACHE,
    prefix=nested_gallery_prefix,
    depth=2,
    access_key=STORAGE_S3_AWS_ACCESS_KEY_ID,
    secret_key=STORAGE_S3_AWS_SECRET_ACCESS_KEY,
)

nested_10001_gallery_prefix = f"{STORAGE_TESTS}/{STORAGE_TESTS_GALLERIES}/nested_10001/"
nested_10001_gallery_storage_name = "tests nested 10001 galleries"
nested_10001_gallery_storage = StorageMinioCreate(
    category=StorageCategoryEnum.gallery,
    name=nested_10001_gallery_storage_name,
    endpoint=STORAGE_S3_ENDPOINT_URL,
    bucket_name=STORAGE_CACHE,
    prefix=nested_10001_gallery_prefix,
    depth=2,
    access_key=STORAGE_S3_AWS_ACCESS_KEY_ID,
    secret_key=STORAGE_S3_AWS_SECRET_ACCESS_KEY,
)


def generate_image(
    size: Tuple[int, int], rgb: Tuple[int, int, int], format: str
) -> bytes:
    img = Image.new("RGB", size, rgb)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format=format)
    return img_bytes.getvalue()


async def generate_gallery(storage_session: AsyncS3Session, gallery: Gallery):
    if not gallery.path:
        return

    faker = ZetsuBouFaker()

    gallery_tag_path = gallery.get_joined_source(DIR_FNAME, TAG_FNAME)
    await storage_session.put_json(gallery_tag_path, gallery.model_dump())

    for i in range(gallery.attributes.pages):
        page = i + 1
        size = faker.image_size()
        rgb = (
            faker.random_int(min=0, max=255),
            faker.random_int(min=0, max=255),
            faker.random_int(min=0, max=255),
        )
        file_format, pil_format, content_type = faker.image_format()

        image_bytes = generate_image(size, rgb, pil_format)

        name = f"{page}{file_format}"
        image_source = gallery.get_joined_source(name)
        await storage_session.put_object(
            image_source, image_bytes, content_type=content_type
        )


async def _generate_galleries(
    storage: StorageMinioCreate,
    callback: Callable[[StorageMinio, AsyncS3Session], Awaitable[None]],
    **kwargs,
):
    created_storage = await CrudStorageMinio.safe_create(storage)
    storage_session = await get_storage_session_by_source(created_storage.source)
    async with storage_session:
        ping = await storage_session.ping()
        if not ping:
            return

        async for _ in storage_session.iter_directories(
            created_storage.source, storage.depth
        ):
            break
        else:
            await callback(created_storage, storage_session, **kwargs)


async def _generate_delete_galleries(
    storage: StorageMinio, storage_session: AsyncS3Session
):
    faker = ZetsuBouFaker()
    gallery = faker.random_minimum_gallery()
    gallery_folder_name = faker.uuid4()
    gallery.path = f"{storage.path}{gallery_folder_name}/"
    await generate_gallery(storage_session, gallery)


async def generate_delete_galleries(
    storage: StorageMinioCreate = delete_gallery_storage,
):
    await _generate_galleries(storage, _generate_delete_galleries)


async def _generate_simple_galleries(
    storage: StorageMinio, storage_session: AsyncS3Session
):
    faker = ZetsuBouFaker()
    galleries = faker.simple_galleries()
    for gallery in galleries:
        gallery_folder_name = faker.uuid4()
        gallery.path = f"{storage.path}{gallery_folder_name}/"
        await generate_gallery(storage_session, gallery)


async def generate_simple_galleries(
    storage: StorageMinioCreate = simple_gallery_storage,
):
    await _generate_galleries(storage, _generate_simple_galleries)


async def _generate_nested_galleries(
    storage: StorageMinio,
    storage_session: AsyncS3Session,
    layer_1_length: int = 2,
    layer_2_length: int = 2,
):
    faker = ZetsuBouFaker()
    layer_1_names = [faker.random_string() for _ in range(layer_1_length)]

    for layer_1_name in layer_1_names:
        for _ in range(layer_2_length):
            gallery = faker.random_minimum_gallery()
            gallery_folder_name = faker.uuid4()
            gallery.path = f"{storage.path}{layer_1_name}/{gallery_folder_name}/"
            await generate_gallery(storage_session, gallery)


async def generate_nested_galleries(
    storage: StorageMinioCreate = nested_gallery_storage,
):
    await _generate_galleries(storage, _generate_nested_galleries)


async def generate_nested_10001_galleries(
    storage: StorageMinioCreate = nested_10001_gallery_storage,
):
    await _generate_galleries(
        storage, _generate_nested_galleries, layer_1_length=100, layer_2_length=101
    )
