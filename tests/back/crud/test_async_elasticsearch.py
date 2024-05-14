from asyncio import Future
from unittest.mock import Mock

import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import HTTPException

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from lib.faker import ZetsuBouFaker
from lib.zetsubou.exceptions import SessionNotFoundException


def test_analyzer():
    faker = ZetsuBouFaker()
    keyword_analyzers = {faker.random_string(): []}
    with pytest.raises(HTTPException):
        CrudAsyncElasticsearchBase(keyword_analyzers=keyword_analyzers)


@pytest.mark.asyncio(scope="session")
async def test_not_implemented_error():
    faker = ZetsuBouFaker()
    crud = CrudAsyncElasticsearchBase()
    with pytest.raises(NotImplementedError):
        await crud.get_by_id(faker.random_string())

    with pytest.raises(NotImplementedError):
        await crud.advanced_search()

    with pytest.raises(NotImplementedError):
        await crud.match_phrase_prefix("")


@pytest.mark.asyncio(scope="session")
async def test_session_not_found_exception():
    faker = ZetsuBouFaker()

    crud = CrudAsyncElasticsearchBase()
    with pytest.raises(SessionNotFoundException):
        await crud.get_field_names()

    with pytest.raises(SessionNotFoundException):
        await crud.get_source_by_id(faker.random_string())

    with pytest.raises(SessionNotFoundException):
        await crud.get_sources_by_ids([faker.random_string()])

    with pytest.raises(SessionNotFoundException):
        await crud.query(1, {})


@pytest.mark.asyncio(scope="session")
async def test_get_field_names():
    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.return_value.indices.return_value.get_mapping = result
    async with CrudAsyncElasticsearchBase() as crud:
        field_names = await crud.get_field_names()
        assert len(field_names) == 0


@pytest.mark.parametrize(
    ("page", "size", "from_"),
    [(1, 10, 0), (1, 100, 0), (2, 100, 100), (0, 10, 0), (0, 100, 0), (-1, 10, 0)],
)
def test_get_from(page: int, size: int, from_: int):
    crud = CrudAsyncElasticsearchBase()
    crud_from = crud.get_from(page, size)
    assert crud_from == from_


@pytest.mark.asyncio(scope="session")
async def test_get_source_by_id():
    faker = ZetsuBouFaker()

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.get.return_value = result

    with pytest.raises(HTTPException):
        async with CrudAsyncElasticsearchBase() as crud:
            crud.async_elasticsearch = mock_async_elasticsearch
            await crud.get_source_by_id(faker.random_string())


@pytest.mark.asyncio(scope="session")
async def test_get_source_by_id_exception():

    def _side_effect(**kwargs):
        raise NotFoundError

    faker = ZetsuBouFaker()

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.get.side_effect = _side_effect

    with pytest.raises(HTTPException):
        async with CrudAsyncElasticsearchBase() as crud:
            crud.async_elasticsearch = mock_async_elasticsearch
            await crud.get_source_by_id(faker.random_string())


@pytest.mark.asyncio(scope="session")
async def test_get_sources_by_ids_exception():

    def _side_effect(**kwargs):
        raise NotFoundError

    faker = ZetsuBouFaker()

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    result = Future()
    result.set_result({})
    mock_async_elasticsearch.search.side_effect = _side_effect

    with pytest.raises(HTTPException):
        async with CrudAsyncElasticsearchBase() as crud:
            crud.async_elasticsearch = mock_async_elasticsearch
            await crud.get_sources_by_ids([faker.random_string()])


@pytest.mark.asyncio(scope="session")
async def test_query():
    with pytest.raises(ValueError):
        async with CrudAsyncElasticsearchBase() as crud:
            await crud.query(1, {})
