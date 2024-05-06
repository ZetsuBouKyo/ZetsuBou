import pytest

from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.session import BaseIntegrationSession
from tests.general.summary import print_api_request, print_api_response


@pytest.mark.asyncio(scope="session")
async def test_get_general_setting(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/setting/front/general"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)
