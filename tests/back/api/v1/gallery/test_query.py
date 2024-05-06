from asyncio import Future
from unittest.mock import patch
from urllib.parse import quote

import pytest

from back.db.model import UserElasticSearchQuery
from back.model.elasticsearch import ElasticsearchCountResult
from back.model.gallery import Galleries
from lib.faker import ZetsuBouFaker
from lib.faker.tag import TagCategoryEnum, TagCountryEnum
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.session import SimpleGalleryIntegrationSession
from tests.general.summary import print_api_request, print_api_response, print_divider


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_count_field(client: ZetsuBouAsyncClient):
    field = f"tags.{TagCategoryEnum.COUNTRY.value}.keyword"
    value = TagCountryEnum.US.value
    async with SimpleGalleryIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/count/{field}/{value}"
            print_api_request(request_url, "get")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)
            result = ElasticsearchCountResult(**response.json())
            assert result.count >= 2


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_post_count(client: ZetsuBouAsyncClient):
    field = f"tags.{TagCategoryEnum.COUNTRY.value}.keyword"
    value = TagCountryEnum.US.value
    data = {"body": {"query": {"terms": {field: [value]}}}}
    async with SimpleGalleryIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/count"
            print_api_request(request_url, "post")
            response = await ac.post(request_url, headers=headers, json=data)
            print_api_response(response)
            result = ElasticsearchCountResult(**response.json())
            assert result.count >= 2


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_random(client: ZetsuBouAsyncClient):
    async with SimpleGalleryIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/random"
            print_api_request(request_url, "get")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_post_custom_search(client: ZetsuBouAsyncClient):
    data = {"body": {"query": {"match_all": {}}}}
    async with SimpleGalleryIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/custom-search"
            print_api_request(request_url, "post")
            response = await ac.post(request_url, headers=headers, json=data)
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_advanced_search(client: ZetsuBouAsyncClient):
    keywords = quote("物理")
    params = {"keywords": keywords, "name": keywords, "raw_name": keywords}
    async with SimpleGalleryIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/advanced-search"
            print_api_request(request_url, "get")
            response = await ac.get(request_url, headers=headers, params=params)
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_search(client: ZetsuBouAsyncClient):
    keywords = quote("物理")
    params = {"keywords": keywords}
    async with SimpleGalleryIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/search"
            print_api_request(request_url, "get")
            response = await ac.get(request_url, headers=headers, params=params)
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_search_query_id(client: ZetsuBouAsyncClient):
    with patch(
        "back.api.v1.gallery.query.CrudUserElasticSearchQuery"
    ) as mock_crud_user_query, patch(
        "back.api.v1.gallery.query.CrudAsyncElasticsearchGallery"
    ) as mock_crud_elastic:
        mock_galleries = Future()
        mock_galleries.set_result(Galleries())
        mock_crud_elastic.return_value.__aenter__.return_value.match_by_query.return_value = (
            mock_galleries
        )
        mock_crud_elastic.return_value.__aenter__.return_value.match.return_value = (
            mock_galleries
        )

        faker = ZetsuBouFaker()
        query_id = faker.random_int()
        user_id = faker.random_int()

        mock_results = [
            None,
            UserElasticSearchQuery(
                id=query_id,
                user_id=user_id,
                name=faker.random_string(),
                query={},
                created=faker.random_datetime_str(),
                modified=faker.random_datetime_str(),
            ),
            UserElasticSearchQuery(
                id=query_id,
                user_id=user_id,
                name=faker.random_string(),
                query={"body": {}},
                created=faker.random_datetime_str(),
                modified=faker.random_datetime_str(),
            ),
        ]

        params = {"query_id": query_id}
        async with SimpleGalleryIntegrationSession():
            headers = get_admin_headers()
            async with client as ac:
                for result in mock_results:
                    return_value = Future()
                    return_value.set_result(result)
                    mock_crud_user_query.get_row_by_id_and_user_id.return_value = (
                        return_value
                    )

                    request_url = f"/api/v1/gallery/search"
                    print_api_request(request_url, "get")
                    response = await ac.get(request_url, headers=headers, params=params)
                    print_api_response(response)

                    galleries = Galleries(**response.json())
                    assert len(galleries.hits.hits) == 0
