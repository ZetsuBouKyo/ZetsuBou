from asyncio import Future
from typing import List
from unittest.mock import Mock, patch

import pytest
from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from fastapi import HTTPException

from back.crud.async_tag import CrudAsyncElasticsearchTag, CrudTag
from back.db.crud import CrudTagAttribute
from back.db.model import TagAttribute, TagAttributeCreate
from back.db.table import TagCategoryBase
from back.model.tag import (
    Tag,
    TagAttributeWithValue,
    TagCreate,
    TagElasticsearch,
    TagInsert,
    TagToken,
    TagUpdate,
)
from lib.faker import ZetsuBouFaker
from tests.general.mock import (
    MockAsyncDatabaseSession,
    MockAsyncIter,
    get_mock_result,
    get_mock_sqlalchemy_async_session,
)
from tests.general.session import BaseIntegrationSession


@pytest.mark.asyncio(scope="session")
async def test_crud_async_elasticsearch_tag():
    async with CrudAsyncElasticsearchTag() as crud:
        crud.get_keyword_fields(None)


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_update_array():
    mock_session = get_mock_sqlalchemy_async_session()

    crud = CrudTag()
    with pytest.raises(HTTPException):
        await crud._update_array(mock_session, 1, [2, 3], [], None)

    await crud._update_array(mock_session, 1, [], [2, 3], TagCategoryBase)


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_update_representative():
    mock_session = get_mock_sqlalchemy_async_session()
    crud = CrudTag()
    with pytest.raises(HTTPException):
        await crud._update_representative(mock_session, 1, 2)

    mock_result = get_mock_result({"id": 1, "linked_id": 2, "token_id": 3})
    mock_session = get_mock_sqlalchemy_async_session(mock_result=mock_result)
    await crud._update_representative(mock_session, 1, 2)


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_check_attribures():
    faker = ZetsuBouFaker()
    mock_session = get_mock_sqlalchemy_async_session()
    crud = CrudTag()
    with pytest.raises(HTTPException):
        await crud._check_attribures(
            mock_session,
            TagInsert(
                id=faker.random_int(),
                name=faker.random_string(),
                attributes={faker.random_int(): faker.sentence()},
            ),
        )


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_get_row_by_id_by_elasticsearch():
    def _side_effect(**kwargs):
        raise NotFoundError

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    mock_async_elasticsearch.get.side_effect = _side_effect
    crud = CrudTag(async_elasticsearch=mock_async_elasticsearch)
    row = await crud.get_row_by_id_by_elasticsearch(1)
    assert row is None

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    value = Future()
    value.set_result({})
    mock_async_elasticsearch.get.return_value = value
    crud = CrudTag(async_elasticsearch=mock_async_elasticsearch)
    row = await crud.get_row_by_id_by_elasticsearch(1)
    assert row is None


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_get_row_by_id():
    faker = ZetsuBouFaker()
    tag_id = faker.random_int()
    tag_name = faker.random_string()

    with patch.object(CrudTag, "get_row_by_id_by_elasticsearch") as mock_crud_tag:
        mock_crud_tag.return_value = None
        crud = CrudTag()
        row = await crud.get_row_by_id_by_elasticsearch(tag_id)
        assert row is None

        with patch("back.crud.async_tag.CrudTagToken") as mock_crud_tag_token:
            value = Future()
            value.set_result(None)
            mock_crud_tag_token.get_row_by_id.return_value = value
            row = await crud.get_row_by_id(tag_id)
            assert row is None

        with patch("back.crud.async_tag.CrudTagToken") as mock_crud_tag_token:
            value = Future()
            value.set_result(TagToken(id=tag_id, name=tag_name))
            mock_crud_tag_token.get_row_by_id.return_value = value
            row = await crud.get_row_by_id(tag_id)
            assert row is None

    with patch.object(CrudTag, "get_row_by_id_by_elasticsearch") as mock_crud_tag:
        mock_crud_tag.return_value = TagElasticsearch(id=tag_id)
        crud = CrudTag()
        row = await crud.get_row_by_id_by_elasticsearch(tag_id)
        assert row is not None

        with patch("back.crud.async_tag.CrudTagToken") as mock_crud_tag_token:
            value = Future()
            value.set_result(None)
            mock_crud_tag_token.get_row_by_id.return_value = value
            row = await crud.get_row_by_id(tag_id)
            assert row is None

        with patch("back.crud.async_tag.CrudTagToken") as mock_crud_tag_token:
            value = Future()
            value.set_result(TagToken(id=tag_id, name=tag_name))
            mock_crud_tag_token.get_row_by_id.return_value = value
            row = await crud.get_row_by_id(tag_id)
            assert row is not None


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_get_interpretation_by_id():
    faker = ZetsuBouFaker()
    tag_id = faker.random_int()
    tag_attributes = {faker.random_int(): faker.sentence()}

    with patch.object(CrudTag, "get_row_by_id_by_elasticsearch") as mock_crud_tag:
        mock_crud_tag.return_value = None
        crud = CrudTag()
        row = await crud.get_row_by_id_by_elasticsearch(tag_id)
        assert row is None

        tag = await crud.get_interpretation_by_id(tag_id)
        assert tag is None

    with patch.object(CrudTag, "get_row_by_id_by_elasticsearch") as mock_crud_tag:
        mock_crud_tag.return_value = TagElasticsearch(
            id=tag_id, attributes=tag_attributes
        )
        crud = CrudTag()
        row = await crud.get_row_by_id_by_elasticsearch(tag_id)
        assert row is not None

        with patch("back.crud.async_tag.CrudTagToken") as mock_crud_tag_token:
            value = Future()
            value.set_result(None)
            mock_crud_tag_token.get_row_by_id.return_value = value
            row = await crud.get_row_by_id(tag_id)
            assert row is None

            with patch(
                "back.crud.async_tag.CrudTagAttribute"
            ) as mock_crud_tag_attribute:
                value = Future()
                value.set_result(None)
                mock_crud_tag_attribute.get_row_by_id.return_value = value
                row = await crud.get_row_by_id(tag_id)
                assert row is None

                tag = await crud.get_interpretation_by_id(tag_id)
                assert tag is None


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_get_interpretations_by_name():
    faker = ZetsuBouFaker()
    tag_id = faker.random_int()
    with patch.object(CrudTag, "get_interpretation_by_id") as mock_crud_tag:
        mock_crud_tag.return_value = None
        crud = CrudTag()
        row = await crud.get_interpretation_by_id(tag_id)
        assert row is None

        with patch("back.crud.async_tag.CrudTagToken") as mock_crud_tag_token:
            value = Future()
            tokens = [TagToken(id=tag_id, name=faker.random_string())]
            value.set_result(tokens)
            mock_crud_tag_token.get_rows_by_name_order_by_id.return_value = value
            tags = await crud.get_interpretations_by_name(tag_id)
            assert len(tags) == 1


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_delete_related_elasticsearch_docs():
    faker = ZetsuBouFaker()
    tag_id = faker.random_int()

    with patch("back.crud.async_tag.async_scan") as mock_async_scan:
        mock_async_scan.return_value = MockAsyncIter(
            [{}, {"_source": {"id": tag_id}}, {"_source": {"id": tag_id}}]
        )

        with patch("back.crud.async_tag.async_bulk") as mock_async_bulk:
            value = Future()
            value.set_result(None)
            mock_async_bulk.return_value = value

            crud = CrudTag(batch_size=1)
            await crud.delete_related_elasticsearch_docs(tag_id)

            crud = CrudTag()
            await crud.delete_related_elasticsearch_docs(tag_id)


@pytest.mark.asyncio(scope="session")
async def test_crud_tag_delete_by_id():
    faker = ZetsuBouFaker()
    tag_id = faker.random_int()

    def _side_effect(**kwargs):
        raise NotFoundError

    mock_async_elasticsearch = Mock(spec=AsyncElasticsearch)
    mock_async_elasticsearch.delete.side_effect = _side_effect

    mock_async_database = MockAsyncDatabaseSession()

    with patch.object(CrudTag, "delete_related_elasticsearch_docs") as mock_crud_tag:
        mock_crud_tag.return_value = None
        crud = CrudTag(
            async_database=mock_async_database,
            async_elasticsearch=mock_async_elasticsearch,
        )

        await crud.delete_by_id(tag_id)


async def _test_insert_tag(tag: Tag):
    crud = CrudTag()
    tag_to_insert = TagInsert(
        id=tag.id,
        name=tag.name,
        category_ids=[c.id for c in tag.categories],
        synonym_ids=[s.id for s in tag.synonyms],
        representative_id=(
            tag.representative.id if tag.representative is not None else None
        ),
        attributes={a.id: a.value for a in tag.attributes},
    )
    await crud.insert(tag_to_insert)
    tag_inserted = await crud.get_interpretation_by_id(tag.id)

    assert tag_inserted.id == tag.id
    assert tag_inserted.name == tag.name

    assert len(tag_inserted.categories) == len(tag.categories)
    assert len(tag_inserted.synonyms) == len(tag.synonyms)
    assert len(tag_inserted.attributes) == len(tag.attributes)

    tag_category_table = {c.id: c.name for c in tag.categories}
    tag_inserted_category_table = {c.id: c.name for c in tag_inserted.categories}
    assert tag_category_table == tag_inserted_category_table

    tag_synonym_table = {s.id: s.name for s in tag.synonyms}
    tag_inserted_synonym_table = {s.id: s.name for s in tag_inserted.synonyms}
    assert tag_synonym_table == tag_inserted_synonym_table

    tag_attribute_table = {a.id: a.value for a in tag.attributes}
    tag_inserted_attribute_table = {a.id: a.value for a in tag_inserted.attributes}
    assert tag_attribute_table == tag_inserted_attribute_table

    if tag_inserted.representative is None:
        assert tag_inserted.representative == tag.representative
    else:
        assert tag_inserted.representative.id == tag.representative.id
        assert tag_inserted.representative.name == tag.representative.name


@pytest.mark.asyncio(scope="session")
@pytest.mark.integration
async def test_crud_tag():
    faker = ZetsuBouFaker()
    num_tag_attribute = 2
    num_tag_category = 2
    num_tag_synonym = 2

    async with BaseIntegrationSession():
        # create the tag attributes
        tag_attributes: List[TagAttribute] = []
        for _ in range(num_tag_attribute):
            tag_attribute = await CrudTagAttribute.create(
                TagAttributeCreate(name=faker.random_string())
            )
            tag_attributes.append(tag_attribute)

        # create the tag
        crud = CrudTag()
        tag_categories: List[TagInsert] = []
        for _ in range(num_tag_category):
            tag = await crud.create(TagCreate(name=faker.random_string()))
            tag_categories.append(tag)
        tag_synonyms: List[TagInsert] = []
        for _ in range(num_tag_synonym):
            tag = await crud.create(TagCreate(name=faker.random_string()))
            tag_synonyms.append(tag)

        tag_representative = await crud.create(TagCreate(name=faker.random_string()))

        # test: create
        tag_1_name = faker.random_string()
        tag_1 = await crud.create(TagCreate(name=tag_1_name))
        assert len(tag_1.category_ids) == 0
        assert len(tag_1.synonym_ids) == 0
        assert tag_1.representative_id is None
        assert tag.attributes == {}

        # test: insert
        await _test_insert_tag(
            Tag(
                id=tag_1.id,
                name=tag_1.name,
                categories=[TagToken(id=t.id, name=t.name) for t in tag_categories],
                synonyms=[TagToken(id=s.id, name=s.name) for s in tag_synonyms],
                representative=TagToken(
                    id=tag_representative.id, name=tag_representative.name
                ),
                attributes=[
                    TagAttributeWithValue(id=a.id, name=a.name, value=faker.sentence())
                    for a in tag_attributes
                ],
            )
        )
        await _test_insert_tag(
            Tag(
                id=tag_1.id,
                name=tag_1.name,
                categories=[
                    TagToken(id=tag_categories[0].id, name=tag_categories[0].name)
                ],
                synonyms=[TagToken(id=tag_synonyms[0].id, name=tag_synonyms[0].name)],
                representative=None,
                attributes=[
                    TagAttributeWithValue(
                        id=tag_attributes[0].id,
                        name=tag_attributes[0].name,
                        value=faker.sentence(),
                    )
                ],
            )
        )
        await _test_insert_tag(
            Tag(
                id=tag_1.id,
                name=tag_1.name,
                categories=[TagToken(id=t.id, name=t.name) for t in tag_categories],
                synonyms=[TagToken(id=s.id, name=s.name) for s in tag_synonyms],
                representative=TagToken(
                    id=tag_representative.id, name=tag_representative.name
                ),
                attributes=[
                    TagAttributeWithValue(id=a.id, name=a.name, value=faker.sentence())
                    for a in tag_attributes
                ],
            )
        )
        await _test_insert_tag(Tag(id=tag_1.id, name=tag_1.name))

        # test: get_interpretations_by_name
        tags_1_by_name_1 = await crud.get_interpretations_by_name(tag_1_name)
        tags_1_num_1 = len(tags_1_by_name_1)

        tag_2 = await crud.create(TagCreate(name=tag_1_name))

        tags_1_by_name_2 = await crud.get_interpretations_by_name(tag_1_name)
        tags_1_num_2 = len(tags_1_by_name_2)
        assert tags_1_num_1 + 1 == tags_1_num_2

        # test: update
        tag_2_category_ids = [tag_categories[0].id]
        tag_2_synonym_ids = [tag_synonyms[0].id]
        tag_2_representative_id = tag_representative.id
        tag_2_updated = await crud.update(
            TagUpdate(
                id=tag_2.id,
                name=tag_1_name,
                category_ids=tag_2_category_ids,
                synonym_ids=tag_2_synonym_ids,
                representative_id=tag_2_representative_id,
            )
        )
        assert tag_2_updated.category_ids == tag_2_category_ids
        assert tag_2_updated.synonym_ids == tag_2_synonym_ids
        assert tag_2_updated.representative_id == tag_2_representative_id

        # delete the tag categories
        for tag in tag_categories:
            await crud.delete_by_id(tag.id)

        tag_2_after_deleting_categories = await crud.get_row_by_id_by_elasticsearch(
            tag_2.id
        )
        assert len(tag_2_after_deleting_categories.category_ids) == 0

        # delete the tag synonyms
        for tag in tag_synonyms:
            await crud.delete_by_id(tag.id)

        tag_2_after_deleting_synonyms = await crud.get_row_by_id_by_elasticsearch(
            tag_2.id
        )
        assert len(tag_2_after_deleting_synonyms.synonym_ids) == 0

        # delete the representative tag
        await crud.delete_by_id(tag_representative.id)

        tag_2_after_deleting_representative_tag = (
            await crud.get_row_by_id_by_elasticsearch(tag_2.id)
        )
        assert tag_2_after_deleting_representative_tag.representative_id is None

        # delete the tags
        await crud.delete_by_id(tag_1.id)
        await crud.delete_by_id(tag_2.id)

        # delete the tag attributes
        for tag_attribute in tag_attributes:
            await CrudTagAttribute.delete_by_id(tag_attribute.id)


@pytest.mark.asyncio(scope="session")
async def test_temp():
    from elasticsearch.helpers import async_scan

    from back.model.elasticsearch import ElasticsearchSearchResult
    from back.session.async_elasticsearch import get_async_elasticsearch
    from back.settings import setting

    index = setting.elastic_index_tag
    print(index)
    async_elasticsearch = get_async_elasticsearch()
    tag_id = 691
    query = {
        "query": {
            "bool": {
                "should": [
                    {"term": {"category_ids": {"value": tag_id}}},
                    {"term": {"synonym_ids": {"value": tag_id}}},
                    {"term": {"representative_id": {"value": tag_id}}},
                ]
            }
        }
    }
    print("hello world")
    async for doc in async_scan(
        client=async_elasticsearch, query=query, index=index, size=10
    ):
        print(doc)
        hits = ElasticsearchSearchResult(**doc)
        for hit in hits.hits.hits:
            print(hit)
    await async_elasticsearch.close()
