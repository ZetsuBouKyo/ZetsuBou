import pytest

from back.db.model import SettingFrontGalleryInterpretation, SettingFrontGalleryUpdate
from lib.faker.tag import TagCategoryEnum
from lib.httpx import ZetsuBouAsyncClient
from tests.general.api import get_admin_headers
from tests.general.session import BaseIntegrationSession, TagIntegrationSession
from tests.general.summary import print_api_request, print_api_response, print_divider


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_startswith_category(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = "/api/v1/setting/front/gallery/category-startswith"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_startswith_tag_field(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = "/api/v1/setting/front/gallery/tag-field-startswith"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_get_interpretation(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = "/api/v1/setting/front/gallery/interpretation"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_reset_settings(client: ZetsuBouAsyncClient):
    async with BaseIntegrationSession():
        headers = get_admin_headers()
        async with client as ac:
            request_url = "/api/v1/setting/front/gallery/reset"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)


@pytest.mark.asyncio(scope="session")
async def test_put_settings(client: ZetsuBouAsyncClient):
    async with TagIntegrationSession() as session:
        headers = get_admin_headers()
        async with client as ac:
            tag_id_1 = session.tags[TagCategoryEnum.COUNTRY.value]
            tag_id_2 = session.tags[TagCategoryEnum.COLOR.value]
            settings = SettingFrontGalleryUpdate(
                category_ids=[tag_id_1], tag_field_ids=[tag_id_2]
            )
            data = settings.model_dump()
            request_url = "/api/v1/setting/front/gallery"
            print_api_request(request_url, "PUT")
            response = await ac.put(request_url, headers=headers, json=data)
            assert response.status_code == 200
            print_api_response(response)

            print_divider()

            request_url = "/api/v1/setting/front/gallery/interpretation"
            print_api_request(request_url, "GET")
            response = await ac.get(request_url, headers=headers)
            assert response.status_code == 200
            print_api_response(response)

            settings_updated = SettingFrontGalleryInterpretation(**response.json())
            category_ids_updated = set([c.id for c in settings_updated.categories])
            tag_field_ids_updated = set([f.id for f in settings_updated.tag_fields])

            assert category_ids_updated == set(settings.category_ids)
            assert tag_field_ids_updated == set(settings.tag_field_ids)
