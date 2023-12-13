import pytest

from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers


@pytest.mark.asyncio(scope="session")
async def test_get_query_examples(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        response = await ac.get("/api/v1/elasticsearch/query-examples", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_get_analyzers(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        response = await ac.get("/api/v1/elasticsearch/analyzers", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_get_gallery_field_names(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        response = await ac.get(
            "/api/v1/elasticsearch/gallery/field-names", headers=headers
        )
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
async def test_get_video_field_names(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        response = await ac.get(
            "/api/v1/elasticsearch/video/field-names", headers=headers
        )
    assert response.status_code == 200
