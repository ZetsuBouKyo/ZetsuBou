import pytest

from lib.faker import ZetsuBouFaker
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_cookies, get_admin_headers
from tests.general.logger import logger
from tests.general.session import SimpleGalleryIntegrationSession
from tests.general.summary import print_api_request, print_api_response, print_divider


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_crud(client: ZetsuBouAsyncClient):
    async with SimpleGalleryIntegrationSession() as session:
        first_gallery = session.galleries[0]
        first_gallery_id = first_gallery.id

        cookies = get_admin_cookies()
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/{first_gallery_id}/images"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            print_api_response(response)

            first_gallery_images = response.json()
            assert len(first_gallery_images) == first_gallery.attributes.pages

            print_divider()

            request_url = f"/api/v1/gallery/{first_gallery_id}/cover"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, cookies=cookies)
            print_api_response(response)

            print_divider()

            request_url = (
                f"/api/v1/gallery/{first_gallery_id}/i/{first_gallery_images[0]}"
            )
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, cookies=cookies)
            print_api_response(response)
