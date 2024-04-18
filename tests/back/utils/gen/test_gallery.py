import pytest
from rich import print_json

from back.db.crud import CrudStorageMinio
from back.model.gallery import Gallery
from back.session.storage import get_storage_session_by_source
from back.settings import setting
from back.utils.gen.gallery import (
    generate_nested_galleries,
    generate_simple_galleries,
    nested_gallery_storage,
    simple_gallery_storage,
)
from lib.faker import ZetsuBouFaker

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname


@pytest.mark.asyncio(scope="session")
async def test_generate_simple_galleries():
    faker = ZetsuBouFaker()
    galleries = faker.simple_galleries()

    await generate_simple_galleries()
    storage = await CrudStorageMinio.safe_create(simple_gallery_storage)
    storage_session = await get_storage_session_by_source(storage.source)

    async with storage_session:
        ping = await storage_session.ping()
        if not ping:
            return

        c = 0
        async for gallery_source in storage_session.iter_directories(
            storage.source, storage.depth
        ):
            gallery_tag_source = gallery_source.get_joined_source(DIR_FNAME, TAG_FNAME)
            gallery_tag = await storage_session.get_json(gallery_tag_source)
            print_json(data=gallery_tag)
            gallery_from_minio = Gallery(**gallery_tag)
            gallery_from_faker = faker.simple_gallery_by_name(gallery_from_minio.name)
            assert gallery_from_faker is not None

            images = await storage_session.list_images(gallery_from_minio)
            assert len(images) == gallery_from_minio.attributes.pages

            c += 1

        assert c == len(galleries)


@pytest.mark.asyncio(scope="session")
async def test_generate_nested_galleries():
    await generate_nested_galleries()

    storage = await CrudStorageMinio.safe_create(nested_gallery_storage)
    storage_session = await get_storage_session_by_source(storage.source)

    async with storage_session:
        ping = await storage_session.ping()
        if not ping:
            return

        c = 0
        async for _ in storage_session.iter_directories(storage.source, storage.depth):
            c += 1

    assert c == 4
