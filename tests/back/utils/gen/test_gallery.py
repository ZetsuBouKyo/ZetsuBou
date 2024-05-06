from typing import Awaitable, Callable
from unittest.mock import patch

import pytest
from rich import print_json

from back.db.crud import CrudStorageMinio
from back.db.model import StorageMinio, StorageMinioCreate
from back.model.gallery import Gallery
from back.session.storage import get_storage_session_by_source
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from back.utils.gen.gallery import (
    _generate_galleries,
    delete_gallery_storage,
    generate_delete_galleries,
    generate_gallery,
    generate_nested_10001_galleries,
    generate_nested_galleries,
    generate_simple_galleries,
    nested_gallery_storage,
    simple_gallery_storage,
)
from lib.faker import ZetsuBouFaker
from lib.zetsubou.exceptions import NotEmptyException, ServicesNotFoundException
from tests.general.logging import logger

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname


@pytest.mark.asyncio(scope="session")
async def test_generate_gallery_none():
    gallry = Gallery()
    await generate_gallery(None, gallry)


@pytest.mark.asyncio(scope="session")
async def test_generate_galleries():
    with patch("back.utils.gen.gallery.get_storage_session_by_source") as mock:
        instance: AsyncS3Session = mock.return_value
        instance.ping.return_value = False

        async def callback(): ...

        with pytest.raises(Exception):
            await _generate_galleries(simple_gallery_storage, callback)


async def _test_generate_galleries(
    storage: StorageMinioCreate,
    callback: Callable[[StorageMinio, AsyncS3Session], Awaitable[None]],
):
    created_storage = await CrudStorageMinio.safe_create(storage)
    storage_session = await get_storage_session_by_source(created_storage.source)

    async with storage_session:
        ping = await storage_session.ping()
        if not ping:
            raise ServicesNotFoundException
        await storage_session.delete(created_storage.source)
        await callback(created_storage, storage_session)
        await storage_session.delete(created_storage.source)


async def _test_generate_delete_galleries(
    storage: StorageMinio, storage_session: AsyncS3Session
):
    c = 0
    to_delete_gallery_source = None
    async for gallery_source in storage_session.iter_directories(
        storage.source, storage.depth
    ):
        to_delete_gallery_source = gallery_source
        logger.info(f"gallery path: {gallery_source.path}")
        c += 1

        assert c == 1
        assert to_delete_gallery_source is not None

    await storage_session.delete(storage.source)
    async for gallery_source in storage_session.iter_directories(
        storage.source, storage.depth
    ):
        raise NotEmptyException


@pytest.mark.asyncio(scope="session")
@pytest.mark.gen
@pytest.mark.integration
async def test_generate_delete_galleries():
    await generate_delete_galleries()
    await generate_delete_galleries()  # generate again
    await _test_generate_galleries(
        delete_gallery_storage, _test_generate_delete_galleries
    )


async def _test_generate_simple_galleries(
    storage: StorageMinio, storage_session: AsyncS3Session
):
    await generate_simple_galleries()

    faker = ZetsuBouFaker()
    galleries = faker.simple_galleries()

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
@pytest.mark.gen
@pytest.mark.integration
async def test_generate_simple_galleries():
    await _test_generate_galleries(
        simple_gallery_storage, _test_generate_simple_galleries
    )


async def _test_generate_nested_galleries(
    storage: StorageMinio, storage_session: AsyncS3Session
):
    await generate_nested_galleries()
    c = 0
    async for _ in storage_session.iter_directories(storage.source, storage.depth):
        c += 1
    assert c == 4


@pytest.mark.asyncio(scope="session")
@pytest.mark.gen
@pytest.mark.integration
async def test_generate_nested_galleries():
    await _test_generate_galleries(
        nested_gallery_storage, _test_generate_nested_galleries
    )


@pytest.mark.asyncio(scope="session")
async def test_generate_nested_10001_galleries():
    with patch("back.utils.gen.gallery._generate_galleries"):
        await generate_nested_10001_galleries()
