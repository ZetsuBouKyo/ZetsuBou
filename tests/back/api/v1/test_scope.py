import pytest

from back.model.scope import ScopeEnum
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_scopes(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        response = await ac.get("/api/v1/scopes", headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_startswith_scopes(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()

    scope_name = ScopeEnum.elasticsearch_analyzers_get.value
    async with client as ac:
        response = await ac.get(
            "/api/v1/scopes-startswith",
            headers=headers,
            params={"name": scope_name},
        )
    assert response.status_code == 200

    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0].get("name", None) == scope_name
