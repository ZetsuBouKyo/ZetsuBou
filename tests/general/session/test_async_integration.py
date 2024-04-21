from collections import deque

import pytest

from lib.faker import ZetsuBouFaker
from tests.general.session.async_integration import SimpleGalleryIntegrationSession


@pytest.mark.asyncio(scope="session")
async def test_simple_gallery_integration_session():
    faker = ZetsuBouFaker()
    faker_galleries = faker.simple_galleries()
    async with SimpleGalleryIntegrationSession() as session:
        assert len(session.galleries) == len(faker_galleries)
        c = 0
        for faker_gallery in faker_galleries:
            for session_gallery in session.galleries:
                if faker_gallery.name == session_gallery.name:
                    c += 1
                    break
        assert c == len(faker_galleries)
