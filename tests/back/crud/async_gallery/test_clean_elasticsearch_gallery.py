import pytest
from elasticsearch.helpers import async_bulk

from back.crud.async_gallery import clean_elasticsearch_gallery
from back.db.crud import CrudStorageMinio
from back.model.base import SourceProtocolEnum
from back.model.gallery import Gallery
from back.session.async_elasticsearch import get_async_elasticsearch
from back.settings import setting
from lib.faker import ZetsuBouFaker
from tests.general.logging import logger

ELASTICSEARCH_INDEX_GALLERY = setting.elastic_index_gallery


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test():
    faker = ZetsuBouFaker()
    storages = await CrudStorageMinio.get_all_rows_order_by_id()
    storage_id = storages[-1].get("id") + 1
    path = f"{SourceProtocolEnum.MINIO.value}-{storage_id}://{faker.random_string()}/{faker.random_string()}"
    logger.info(f"gallery path: {path}")

    batches = []
    batch_size = 2
    gallery_num = 3

    async_elasticsearch = get_async_elasticsearch()
    for _ in range(gallery_num):
        gallery = Gallery()
        gallery.id = faker.uuid4()
        gallery.path = path
        action = {
            "_index": ELASTICSEARCH_INDEX_GALLERY,
            "_id": gallery.id,
            "_source": gallery.model_dump(),
        }
        batches.append(action)
    await async_bulk(async_elasticsearch, batches)

    await async_elasticsearch.indices.refresh(index=ELASTICSEARCH_INDEX_GALLERY)

    results = await clean_elasticsearch_gallery(
        async_elasticsearch, batch_size=batch_size
    )
    logger.info(f"results: {results.model_dump()}")
    assert results.total > 0
    assert results.storage[gallery._scheme] > 0
    await async_elasticsearch.indices.refresh(index=ELASTICSEARCH_INDEX_GALLERY)

    results = await clean_elasticsearch_gallery(
        async_elasticsearch, batch_size=batch_size
    )
    assert results.total == 0
