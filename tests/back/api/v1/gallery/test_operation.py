import pytest

from lib.httpx import ZetsuBouAsyncClient
from lib.zetsubou.exceptions import NotEmptyException
from tests.general.api import get_admin_headers
from tests.general.session.async_integration import DeleteGalleryIntegrationSession
from tests.general.summary import print_api_request, print_api_response


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_delete(client: ZetsuBouAsyncClient):
    async with DeleteGalleryIntegrationSession() as session:
        gallery_id = session.galleries[0].id
        headers = get_admin_headers()
        async with client as ac:
            request_url = f"/api/v1/gallery/{gallery_id}/delete"
            print_api_request(request_url, "DELETE")
            response = await ac.delete(request_url, headers=headers)
            print_api_response(response)
        async with session.storage_session:
            async for _ in session.storage_session.iter_directories(
                session.storage.source, session.storage.depth
            ):
                raise NotEmptyException
