from typing import List
from unittest.mock import patch

import pytest

from back.crud.async_tag import CrudTag
from back.db.crud import CrudTagAttribute
from back.model.tag import Tag, TagAttribute, TagToken
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
                    TagAttribute(
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
    await generate_tag_attributes()

    faker = ZetsuBouFaker()
    tag_attributes = faker.tag_attributes()
    for tag_attribute_name in tag_attributes:
        tag_attribute = await CrudTagAttribute.get_row_by_name(tag_attribute_name)
        assert tag_attribute is not None
        assert tag_attribute.name == tag_attribute_name

    await delete_tag_attributes()


@pytest.mark.asyncio(scope="session")
@pytest.mark.gen
@pytest.mark.integration
async def test_generate_tags():
    await delete_tags()
    await delete_tags()

    await generate_tags()
    await generate_tags()

    faker = ZetsuBouFaker()
    faker_tags = faker.tags()
    for faker_tag in faker_tags:
        tag = await get_tag(faker_tag)
        assert tag is not None

    await delete_tags()
