from unittest.mock import patch

import pytest

from back.crud.async_tag import CrudTag
from back.model.tag import Tag, TagAttributeWithValue, TagToken
from back.session.async_elasticsearch import get_async_elasticsearch
from back.utils.gen.tag import (
    delete_tag_attributes,
    delete_tags,
    generate_tag_attributes,
    generate_tags,
    get_tag,
)
from lib.faker import ZetsuBouFaker
from lib.faker.tag import FakerTag


@pytest.mark.asyncio(scope="session")
async def test_get_tag():
    with patch("back.utils.gen.tag.CrudTag", spec=CrudTag) as mock:
        faker = ZetsuBouFaker()
        instance: CrudTag = mock.return_value
        tag_name = faker.tags()[0].name
        tags = [
            Tag(
                id=faker.random_int(),
                name=tag_name,
                categories=[
                    TagToken(id=faker.random_int(), name=faker.random_string())
                ],
            ),
            Tag(
                id=faker.random_int(),
                name=tag_name,
                synonyms=[TagToken(id=faker.random_int(), name=faker.random_string())],
            ),
            Tag(
                id=faker.random_int(),
                name=tag_name,
                representative=TagToken(
                    id=faker.random_int(), name=faker.random_string()
                ),
            ),
            Tag(
                id=faker.random_int(),
                name=tag_name,
                attributes=[
                    TagAttributeWithValue(
                        id=faker.random_int(),
                        name=faker.random_string(),
                        value=faker.sentence(),
                    )
                ],
            ),
        ]
        instance.get_interpretations_by_name.return_value = tags
        faker_tag = FakerTag(name=tag_name)
        assert await get_tag(faker_tag) is None


@pytest.mark.asyncio(scope="session")
@pytest.mark.gen
@pytest.mark.integration
async def test_generate_tag_attributes():
    await delete_tag_attributes()
    await delete_tag_attributes()

    await generate_tag_attributes()
    tag_attribute_table = await generate_tag_attributes()

    faker = ZetsuBouFaker()
    tag_attributes = faker.tag_attributes()
    for tag_attribute_name in tag_attributes:
        tag_attribute = tag_attribute_table[tag_attribute_name]
        assert tag_attribute is not None

    await delete_tag_attributes()


@pytest.mark.asyncio(scope="session")
@pytest.mark.gen
@pytest.mark.integration
async def test_generate_tags():
    async_elasticsearch = get_async_elasticsearch()
    await delete_tags(async_elasticsearch=async_elasticsearch)
    await delete_tags(async_elasticsearch=async_elasticsearch)

    await generate_tags(async_elasticsearch=async_elasticsearch)
    tag_table = await generate_tags(async_elasticsearch=async_elasticsearch)

    faker = ZetsuBouFaker()
    faker_tags = faker.tags()
    for faker_tag in faker_tags:
        tag = tag_table[faker_tag.name]
        assert tag is not None

    await delete_tags()
