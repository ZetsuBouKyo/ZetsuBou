import pytest

from back.db.model import StorageMinio
from back.model.storage import StorageCategoryEnum
from back.settings import setting
from lib.faker import ZetsuBouFaker
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.summary import print_api_request, print_api_response, print_divider

ENDPOINT = setting.storage_s3_endpoint_url
ACCESS_KEY = setting.storage_s3_aws_access_key_id
SECRET_KEY = setting.storage_s3_aws_secret_access_key


@pytest.mark.asyncio(scope="session")
async def test_get_storage_categories(client: ZetsuBouAsyncClient):
    headers = get_admin_headers()
    async with client as ac:
        request_url = "/api/v1/storage/minio/storage-categories"
        print_api_request(request_url, "GET")
        response = await ac.get(request_url, headers=headers)
        print_api_response(response)

        assert response.status_code == 200
        assert response.json() == {"gallery": 0, "video": 1}


@pytest.mark.asyncio(scope="session")
async def test_crud(client: ZetsuBouAsyncClient):
    faker = ZetsuBouFaker()
    headers = get_admin_headers()
    async with client as ac:
        # get total number of storages
        request_url = "/api/v1/storage/minio/total-storages"
        print_api_request(request_url, "GET")
        response = await ac.get(request_url, headers=headers)
        print_api_response(response)

        assert response.status_code == 200
        total_storage_i = int(response.text)

        print_divider()

        # create a storage
        request_url = "/api/v1/storage/minio/storage"
        data = {
            "category": StorageCategoryEnum.gallery.value,
            "name": faker.random_string(),
            "endpoint": faker.url(),
            "bucket_name": faker.random_string(),
            "prefix": "",
            "depth": 1,
            "access_key": faker.random_string(),
            "secret_key": faker.random_string(),
        }
        print_api_request(request_url, "POST")
        response = await ac.post(request_url, headers=headers, json=data)
        print_api_response(response)

        assert response.status_code == 200
        storage = StorageMinio(**response.json())

        print_divider()

        # get the storages
        request_url = "/api/v1/storage/minio/storages"
        params = {"page": 1, "size": 1}
        print_api_request(request_url, "GET", params=params)
        response = await ac.get(request_url, headers=headers, params=params)
        print_api_response(response)

        assert response.status_code == 200
        assert len(response.json()) == 1

        print_divider()

        # update the storage
        new_storage_name = faker.random_string()
        data["id"] = storage.id
        data["name"] = new_storage_name

        request_url = "/api/v1/storage/minio/storage"
        print_api_request(request_url, "PUT", data=data)
        response = await ac.put(request_url, headers=headers, json=data)
        print_api_response(response)

        assert response.status_code == 200

        print_divider()

        # get total number of storages
        request_url = "/api/v1/storage/minio/total-storages"
        print_api_request(request_url, "GET")
        response = await ac.get(request_url, headers=headers)
        print_api_response(response)

        assert response.status_code == 200
        total_storage_f = int(response.text)
        assert total_storage_f == total_storage_i + 1

        print_divider()

        # delete the storage
        request_url = f"/api/v1/storage/minio/storage/{storage.id}"
        print_api_request(request_url, "DELETE")
        response = await ac.delete(request_url, headers=headers)
        print_api_response(response)

        assert response.status_code == 200
