from copy import deepcopy

import pytest

from back.model.gallery import Gallery
from lib.faker import ZetsuBouFaker
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.session.async_integration import DeleteGalleryIntegrationSession
from tests.general.summary import print_api_request, print_api_response


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_tag(client: ZetsuBouAsyncClient):
    faker = ZetsuBouFaker()
    async with DeleteGalleryIntegrationSession() as session:
        gallery = deepcopy(session.galleries[0])
        gallery_id = gallery.id
        headers = get_admin_headers()
        async with client as ac:
            gallery_name = faker.sentence()
            gallery.name = gallery_name
            data = gallery.model_dump()

            request_url = f"/api/v1/gallery/{gallery_id}/tag"
            print_api_request(request_url, "POST")
            response = await ac.post(request_url, headers=headers, json=data)
            print_api_response(response)

            request_url = f"/api/v1/gallery/{gallery_id}/tag"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)

            gallery_updated = Gallery(**response.json())
            assert gallery_updated.name == gallery_name


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_tag_404(client: ZetsuBouAsyncClient):
    faker = ZetsuBouFaker()
    async with DeleteGalleryIntegrationSession() as session:
        gallery = deepcopy(session.galleries[0])
        gallery.id = gallery.id + faker.random_string(number=56)
        gallery_id = gallery.id
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/{gallery_id}/tag"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)

            assert response.status_code == 404


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_post_tag_exception(client: ZetsuBouAsyncClient):
    async with DeleteGalleryIntegrationSession() as session:
        gallery = deepcopy(session.galleries[0])
        gallery_id = gallery.id
        headers = get_admin_headers()
        async with client as ac:
            gallery.id = gallery.id + "1"
            data = gallery.model_dump()

            request_url = f"/api/v1/gallery/{gallery_id}/tag"
            print_api_request(request_url, "POST")
            response = await ac.post(request_url, headers=headers, json=data)
            print_api_response(response)

            assert response.status_code == 409
