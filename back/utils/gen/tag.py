from typing import Dict, Optional

from back.crud.async_tag import CrudTag
from back.db.crud import CrudTagAttribute
from back.db.model import TagAttributeCreate
from back.logging import logger_zetsubou
from back.model.tag import Tag, TagInsert
from back.session.async_elasticsearch import AsyncElasticsearch, get_async_elasticsearch
from lib.faker import ZetsuBouFaker
from lib.faker.tag import FakerTag


async def generate_tag_attributes():
    faker = ZetsuBouFaker()
    for attribute_name in faker.tag_attributes():
        tag_attribute = await CrudTagAttribute.get_row_by_name(attribute_name)
        if tag_attribute is None:
            tag_attribute = await CrudTagAttribute.create(
                TagAttributeCreate(name=attribute_name)
            )
        else:
            logger_zetsubou.info(f"tag attribute: {attribute_name} exists.")


async def delete_tag_attributes():
    faker = ZetsuBouFaker()
    for attribute_name in faker.tag_attributes():
        tag_attribute = await CrudTagAttribute.get_row_by_name(attribute_name)
        if tag_attribute is not None:
            await CrudTagAttribute.delete_by_id(tag_attribute.id)


async def get_tag(
    faker_tag: FakerTag,
    async_elasticsearch: AsyncElasticsearch = get_async_elasticsearch(),
) -> Optional[Tag]:
    crud = CrudTag(async_elasticsearch=async_elasticsearch)
    existing_tags = await crud.get_interpretations_by_name(faker_tag.name)
    faker_tag_categories = set(faker_tag.categories)
    for existing_tag in existing_tags:
        existing_tag_categories = set()
        for existing_tag_category in existing_tag.categories:
            existing_tag_categories.add(existing_tag_category.name)
        if faker_tag_categories != existing_tag_categories:
            continue
        if len(existing_tag.synonyms) != 0:
            continue
        if existing_tag.representative is not None:
            continue
        if len(existing_tag.attributes) != 0:
            continue
        return existing_tag
    return None


async def generate_tags(
    async_elasticsearch: AsyncElasticsearch = get_async_elasticsearch(),
):
    tag_table: Dict[str, int] = {}
    faker = ZetsuBouFaker()
    tags = faker.tags()

    crud = CrudTag(async_elasticsearch=async_elasticsearch)
    for faker_tag in tags:
        existing_tag = await get_tag(faker_tag, async_elasticsearch=async_elasticsearch)
        if existing_tag is not None:
            tag_table[existing_tag.name] = existing_tag.id
            continue
        tag_category_ids = []
        for faker_tag_category in faker_tag.categories:
            tag_category_id = tag_table.get(faker_tag_category, None)
            tag_category_ids.append(tag_category_id)

        inserted_tag = await crud.insert(
            TagInsert(name=faker_tag.name, category_ids=tag_category_ids)
        )
        tag_table[inserted_tag.name] = inserted_tag.id


async def delete_tags(
    async_elasticsearch: AsyncElasticsearch = get_async_elasticsearch(),
):
    faker = ZetsuBouFaker()
    tags = faker.tags()
    tags.reverse()
    crud = CrudTag(async_elasticsearch=async_elasticsearch)
    for faker_tag in tags:
        existing_tag = await get_tag(faker_tag, async_elasticsearch=async_elasticsearch)
        if existing_tag is not None:
            await crud.delete_by_id(existing_tag.id)
