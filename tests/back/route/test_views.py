import pytest

from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_cookies

routes = [
    "/",
    "/gallery/search",
    "/gallery/random",
    "/gallery/advanced-search",
    "/gallery",
    "/video/search",
    "/video/random",
    "/video/advanced-search",
    "/login",
    "/initialization",
    "/bookmark",
    "/bookmark/gallery",
    "/bookmark/video",
    "/settings",
    "/settings/account",
    "/settings/appearance",
    "/settings/authentication",
    "/settings/storage-minio",
    "/settings/system",
    "/settings/elasticsearch-count",
    "/settings/elasticsearch-search",
    "/settings/tag",
    "/settings/tag-token",
    "/settings/tag-attribute",
    "/settings/tag-front-ui",
    "/settings/quest",
    "/settings/elasticsearch-count-quest",
    "/settings/users",
    "/settings/group",
    "/construction",
    "/NotFound",
]


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_admin_user(client: ZetsuBouAsyncClient):
    cookies = get_admin_cookies()
    async with client as ac:
        for route in routes:
            response = await ac.get(route, cookies=cookies)
            assert response.status_code == 200
