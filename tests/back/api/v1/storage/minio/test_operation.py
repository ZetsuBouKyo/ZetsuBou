import pytest

from back.settings import setting
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.summary import print_api_request, print_api_response, print_divider

ENDPOINT = setting.storage_s3_endpoint_url
ACCESS_KEY = setting.storage_s3_aws_access_key_id
SECRET_KEY = setting.storage_s3_aws_secret_access_key


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_minio_list(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        request_url = "/api/v1/storage/minio/list"
        print_api_request(request_url, "GET")
        response = await ac.get(request_url, headers=headers)
        print_api_response(response)

        assert response.status_code == 200
        assert response.json() == []

        print_divider()

        params = {
            "bucket_name": "/",
            "endpoint": ENDPOINT,
            "access_key": ACCESS_KEY,
            "secret_key": SECRET_KEY,
        }
        print_api_request(request_url, "GET", params=params)
        response = await ac.get(
            request_url,
            headers=headers,
            params=params,
        )
        print_api_response(response)

        assert response.status_code == 200
