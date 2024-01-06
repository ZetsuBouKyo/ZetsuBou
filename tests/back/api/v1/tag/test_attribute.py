import pytest

from lib.faker import ZetsuBouFaker
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.logger import logger
from tests.general.summary import print_api_request, print_api_response, print_divider


@pytest.mark.asyncio(scope="session")
async def test_crud(client: ZetsuBouAsyncClient):
    faker = ZetsuBouFaker()
    attrs = [faker.random_string(number=8, is_lower=True) for _ in range(5)]
    attr_ids = []
    headers = get_admin_headers()
    async with client as ac:
        for attr in attrs:
            request_url = "/api/v1/tag/attribute"
            data = {"name": attr}
            print_api_request(request_url, "POST", data=data)

            response = await ac.post(request_url, headers=headers, json=data)
            print_api_response(response)

            assert response.status_code == 200

            tag_attr = response.json()
            tag_attr_id = tag_attr.get("id", None)
            assert tag_attr_id is not None

            attr_ids.append(tag_attr_id)

            print_divider()

        request_url = "/api/v1/tag/total-attributes"
        print_api_request(request_url, "GET")
        response = await ac.get(request_url, headers=headers)
        print_api_response(response)
        assert response.status_code == 200
        total = int(response.text)
        assert total > 0
        print_divider()

        request_url = "/api/v1/tag/attribute"
        data = {"id": attr_ids[0], "name": faker.random_string(number=8, is_lower=True)}
        print_api_request(request_url, "PUT", data=data)
        response = await ac.put(request_url, headers=headers, json=data)
        print_api_response(response)
        assert response.status_code == 200
        print_divider()

        request_url = "/api/v1/tag/attributes"
        print_api_request(request_url, "GET")
        response = await ac.get(request_url, headers=headers)
        print_api_response(response)
        assert response.status_code == 200
        assert len(response.json()) > 0
        print_divider()

        for i, id in enumerate(attr_ids):
            request_url = f"/api/v1/tag/attribute/{id}"
            print_api_request(request_url, "DELETE")

            response = await ac.delete(request_url, headers=headers)
            print_api_response(response)

            assert response.status_code == 200

            if i != len(attr_ids) - 1:
                print_divider()
