from asyncio import Future
from unittest.mock import Mock

import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import HTTPException

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from lib.faker import ZetsuBouFaker


def test_crud_async_elasticsearch_base_analyzer():
    faker = ZetsuBouFaker()
    keyword_analyzers = {faker.random_string(): []}
    with pytest.raises(HTTPException):
        CrudAsyncElasticsearchBase(keyword_analyzers=keyword_analyzers)


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_base_not_implemented_error():
    faker = ZetsuBouFaker()
    crud = CrudAsyncElasticsearchBase()
    with pytest.raises(NotImplementedError):
        await crud.get_by_id(faker.random_string())

    with pytest.raises(NotImplementedError):
        await crud.advanced_search()

    with pytest.raises(NotImplementedError):
        await crud.match_phrase_prefix("")


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_base_get_field_names():
    crud = CrudAsyncElasticsearchBase()
    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.return_value.indices.return_value.get_mapping = result
    field_names = await crud.get_field_names()
    assert len(field_names) == 0


@pytest.mark.parametrize(
    ("page", "size", "from_"),
    [(1, 10, 0), (1, 100, 0), (2, 100, 100), (0, 10, 0), (0, 100, 0), (-1, 10, 0)],
)
def test_crud_async_elasticsearch_base_get_from(page: int, size: int, from_: int):
    crud = CrudAsyncElasticsearchBase()
    crud_from = crud.get_from(page, size)
    assert crud_from == from_


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_base_get_source_by_id():
    faker = ZetsuBouFaker()

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.get.return_value = result

    crud = CrudAsyncElasticsearchBase()
    crud.async_elasticsearch = mock_async_elasticsearch

    with pytest.raises(HTTPException):
        await crud.get_source_by_id(faker.random_string())


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_base_get_source_by_id_exception():

    def _side_effect(**kwargs):
        raise NotFoundError

    faker = ZetsuBouFaker()

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.get.side_effect = _side_effect

    crud = CrudAsyncElasticsearchBase()
    crud.async_elasticsearch = mock_async_elasticsearch

    with pytest.raises(HTTPException):
        await crud.get_source_by_id(faker.random_string())


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_base_get_sources_by_ids_exception():

    def _side_effect(**kwargs):
        raise NotFoundError

    faker = ZetsuBouFaker()

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.search.side_effect = _side_effect

    crud = CrudAsyncElasticsearchBase()
    crud.async_elasticsearch = mock_async_elasticsearch

    with pytest.raises(HTTPException):
        await crud.get_sources_by_ids([faker.random_string()])


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_base_query():
    crud = CrudAsyncElasticsearchBase()
    with pytest.raises(ValueError):
        await crud.query(1, {})
