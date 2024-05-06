import pytest

from back.db.crud import CrudScope
from back.db.model import (
    GroupWithScopeIdsSafeCreate,
    GroupWithScopeIdsUpdate,
    GroupWithScopes,
)
from back.model.scope import ScopeEnum
from lib.faker import ZetsuBouFaker
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.session import BaseIntegrationSession
from tests.general.summary import print_api_request, print_api_response, print_divider


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_total_groups(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/total-groups"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_groups(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/groups"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_group(client: ZetsuBouAsyncClient):
    faker = ZetsuBouFaker()
    async with BaseIntegrationSession():
        scope_1 = await CrudScope.get_row_by_name(
            ScopeEnum.elasticsearch_analyzers_get.value
        )
        scope_2 = await CrudScope.get_row_by_name(
            ScopeEnum.elasticsearch_query_examples_get.value
        )

        headers = get_admin_headers()
        async with client as ac:
            group = GroupWithScopeIdsSafeCreate(
                name=faker.random_string(), scope_ids=[scope_1.id, scope_2.id]
            )
            data = group.model_dump()
            request_url = f"/api/v1/group-with-scope-ids"
            print_api_request(request_url, "POST")
            response = await ac.post(request_url, headers=headers, json=data)
            assert response.status_code == 200
            print_api_response(response)
            group_created = GroupWithScopes(**response.json())

            print_divider()

            group_name = faker.random_string()
            group_to_update = GroupWithScopeIdsUpdate(
                id=group_created.id, name=group_name, scope_ids=[scope_1.id]
            )
            data = group_to_update.model_dump()

            request_url = f"/api/v1/group-with-scope-ids"
            print_api_request(request_url, "PUT")
            response = await ac.put(request_url, headers=headers, json=data)
            assert response.status_code == 200
            print_api_response(response)

            print_divider()

            request_url = f"/api/v1/group-with-scopes/{group_created.id}"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)

            print(response.json())

            group_updated = GroupWithScopes(**response.json())
            assert group_updated.name == group_name
            assert set(group_updated.scope_ids) == set(group_to_update.scope_ids)

            print_divider()

            request_url = f"/api/v1/group/{group_created.id}"
            print_api_request(request_url, "DELETE")
            response = await ac.delete(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)
