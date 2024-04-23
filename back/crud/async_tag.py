from typing import Any, List, Optional

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError
from elasticsearch.helpers import async_bulk, async_scan
from fastapi import HTTPException
from sqlalchemy import and_, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.db.crud import CrudTagAttribute, CrudTagToken
from back.db.model import TagRepresentative
from back.db.table import (
    TagAttributeBase,
    TagCategoryBase,
    TagRepresentativeBase,
    TagSynonymBase,
    TagTokenBase,
)
from back.logging import logger_zetsubou
from back.model.elasticsearch import AnalyzerEnum, SearchResult
from back.model.tag import (
    Tag,
    TagAttribute,
    TagCreate,
    TagElasticsearch,
    TagInsert,
    TagInserted,
    TagToken,
    TagUpdate,
)
from back.session.async_db import async_session
from back.session.async_elasticsearch import get_async_elasticsearch
from back.settings import setting

INDEX = setting.elastic_index_tag
BATCH_SIZE = 300
SIZE = 100
ES_SIZE = setting.elastic_size
ELASTICSEARCH_INDEX_TAG = setting.elastic_index_tag


class CrudAsyncElasticsearchTag(CrudAsyncElasticsearchBase[TagElasticsearch]):
    def __init__(
        self,
        hosts: List[str] = None,
        size: int = None,
        index: str = ELASTICSEARCH_INDEX_TAG,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        sorting: List[Any] = ["_score", "id"],
        is_from_setting_if_none: bool = False,
    ):
        super().__init__(
            hosts=hosts,
            size=size,
            index=index,
            analyzer=analyzer,
            sorting=sorting,
            is_from_setting_if_none=is_from_setting_if_none,
        )

    @property
    def fields(self) -> List[str]:
        return ["attributes.*"]


class CrudTag:
    def __init__(
        self,
        async_elasticsearch: AsyncElasticsearch = get_async_elasticsearch(),
        index: str = INDEX,
        size: int = SIZE,
        batch_size: int = BATCH_SIZE,
    ):
        self.async_elasticsearch = async_elasticsearch
        self.index = index
        self.size = size
        self.batch_size = batch_size

    async def _update_array(
        self,
        session: AsyncSession,
        tag_id: int,
        ids_to_add: List[int],
        ids_to_delete: List[int],
        base,
    ):
        if ids_to_add:
            for id in ids_to_add:
                rows = await session.execute(
                    select(TagTokenBase).where(TagTokenBase.id == id)
                )
                first = rows.scalars().first()
                if first is None:
                    raise HTTPException(
                        status_code=404, detail=f"Token id: {id} not found"
                    )

                rows = await session.execute(
                    select(base).where(
                        and_(base.linked_id == id, base.token_id == tag_id)
                    )
                )
                first = rows.scalars().first()
                if first is None:
                    array = base(linked_id=id, token_id=tag_id)
                    session.add(array)

        for id in ids_to_delete:
            await session.execute(
                delete(base).where(and_(base.id == id, base.token_id == tag_id))
            )

    async def _update_categories(
        self,
        session: AsyncSession,
        tag_id: int,
        ids_to_add: List[int],
        ids_to_delete: List[int],
    ):
        await self._update_array(
            session, tag_id, ids_to_add, ids_to_delete, TagCategoryBase
        )

    async def _update_synonyms(
        self,
        session: AsyncSession,
        tag_id: int,
        ids_to_add: List[int],
        ids_to_delete: List[int],
    ):
        await self._update_array(
            session, tag_id, ids_to_add, ids_to_delete, TagSynonymBase
        )

    async def _update_representative(
        self, session: AsyncSession, token_id: int, representative_id: int
    ):
        if representative_id:
            rows = await session.execute(
                select(TagTokenBase).where(TagTokenBase.id == representative_id)
            )
            first = rows.scalars().first()
            if first is None:
                raise HTTPException(
                    status_code=404, detail=f"Token id: {representative_id} not found"
                )

            rows = await session.execute(
                select(TagRepresentativeBase).where(
                    TagRepresentativeBase.token_id == token_id
                )
            )
            first = rows.scalars().first()
            if first is None:
                representative = TagRepresentativeBase(
                    linked_id=representative_id, token_id=token_id
                )
                session.add(representative)
            else:
                representative = TagRepresentative(**first.__dict__)
                representative.linked_id = representative_id
                rows = await session.execute(
                    update(TagRepresentativeBase)
                    .where(TagRepresentativeBase.token_id == token_id)
                    .values(**representative.model_dump())
                )
        else:
            await session.execute(
                delete(TagRepresentativeBase).where(
                    TagRepresentativeBase.token_id == token_id
                )
            )

    async def _check_attribures(self, session: AsyncSession, tag: TagInsert):
        if tag.attributes:
            for attr_id in tag.attributes.keys():
                rows = await session.execute(
                    select(TagAttributeBase).where(TagAttributeBase.id == attr_id)
                )
                first = rows.scalars().first()
                if first is None:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Token Attribute id: {attr_id} not found",
                    )

    async def insert(self, tag: TagInsert) -> TagInserted:
        tag = TagInsert(**tag.model_dump())

        old_tag = None
        if tag.id is not None:
            old_tag = await self.get_row_by_id_by_elasticsearch(tag.id)

        tag_category_ids_set = set(tag.category_ids)
        tag.category_ids = list(tag_category_ids_set)

        tag_synonym_ids_set = set(tag.synonym_ids)
        tag.synonym_ids = list(tag_synonym_ids_set)

        if old_tag is None or not old_tag.category_ids:
            category_ids_to_add = tag.category_ids
            category_ids_to_delete = []

            synonyms_ids_to_add = tag.synonym_ids
            synonyms_ids_to_delete = []
        else:
            old_tag_category_ids_set = set(old_tag.category_ids)
            category_ids_to_add = tag_category_ids_set - old_tag_category_ids_set
            category_ids_to_delete = old_tag_category_ids_set - tag_category_ids_set

            old_tag_synonym_ids_set = set(old_tag.synonym_ids)
            synonyms_ids_to_add = tag_synonym_ids_set - old_tag_synonym_ids_set
            synonyms_ids_to_delete = old_tag_synonym_ids_set - tag_synonym_ids_set

        async with async_session() as session:
            async with session.begin():
                if tag.id is None:
                    token = TagTokenBase(name=tag.name)
                    session.add(token)
                    await session.flush()
                    tag.id = token.id
                    tag.name = token.name
                else:
                    await session.execute(
                        update(TagTokenBase)
                        .where(TagTokenBase.id == tag.id)
                        .values(id=tag.id, name=tag.name)
                    )

                await self._update_categories(
                    session, tag.id, category_ids_to_add, category_ids_to_delete
                )
                await self._update_synonyms(
                    session, tag.id, synonyms_ids_to_add, synonyms_ids_to_delete
                )
                await self._update_representative(
                    session, tag.id, tag.representative_id
                )
                await self._check_attribures(session, tag)
                await session.commit()

        await self.async_elasticsearch.index(
            index=self.index,
            id=tag.id,
            document=TagElasticsearch(**tag.model_dump()).model_dump(),
        )
        return tag

    async def create(self, tag: TagCreate) -> TagInserted:
        return await self.insert(tag)

    async def get_row_by_id_by_elasticsearch(
        self, tag_id: int
    ) -> Optional[TagElasticsearch]:
        try:
            hit = await self.async_elasticsearch.get(index=self.index, id=tag_id)
        except NotFoundError:
            return None
        source = hit.get("_source", None)
        if source is None:
            return None
        return TagElasticsearch(**source)

    async def get_row_by_id(self, tag_id: int) -> Optional[TagInserted]:
        token = await CrudTagToken.get_row_by_id(tag_id)
        elastic_tag = await self.get_row_by_id_by_elasticsearch(tag_id)

        if token is None:
            if elastic_tag is not None:
                logger_zetsubou.warning(
                    f"tag ID: {tag_id} exists in Elasticsearch but not in the database."
                )
            return None
        if elastic_tag is None:
            logger_zetsubou.warning(
                f"tag ID: {tag_id} exists in database but not in the Elasticsearch."
            )
            return None

        elastic_tag = elastic_tag.model_dump()
        elastic_tag["name"] = token.name
        return TagInserted(**elastic_tag)

    async def get_interpretation_by_id(self, tag_id: int) -> Optional[Tag]:
        tag_in_ids = await self.get_row_by_id_by_elasticsearch(tag_id)
        if tag_in_ids is None:
            return None
        token_ids = [tag_in_ids.id] + tag_in_ids.category_ids + tag_in_ids.synonym_ids
        if tag_in_ids.representative_id:
            token_ids.append(tag_in_ids.representative_id)

        inconsistent = False
        token_id_table = {}
        for id in token_ids:
            token = await CrudTagToken.get_row_by_id(id)
            if token is None:
                inconsistent = True
                continue
            token_id_table[token.id] = token.name

        attribute_id_table = {}
        for attribute_id in tag_in_ids.attributes.keys():
            attribute = await CrudTagAttribute.get_row_by_id(attribute_id)
            if attribute is None:
                inconsistent = True
                continue
            attribute_id_table[attribute.id] = attribute.name

        if inconsistent:
            logger_zetsubou.warning(
                f"There is an inconsistency in the tag ID {tag_id} in Elasticsearch."
            )
            return None

        return Tag(
            id=tag_in_ids.id,
            name=token_id_table[tag_in_ids.id],
            categories=[
                TagToken(id=id, name=token_id_table[id])
                for id in tag_in_ids.category_ids
                if token_id_table.get(id, None) is not None
            ],
            synonyms=[
                TagToken(id=id, name=token_id_table[id])
                for id in tag_in_ids.synonym_ids
                if token_id_table.get(id, None) is not None
            ],
            representative=(
                TagToken(
                    id=tag_in_ids.representative_id,
                    name=token_id_table[tag_in_ids.representative_id],
                )
                if tag_in_ids.representative_id
                and token_id_table.get(tag_in_ids.representative_id, None) is not None
                else None
            ),
            attributes=[
                TagAttribute(id=id, name=attribute_id_table[id], value=value)
                for id, value in tag_in_ids.attributes.items()
                if attribute_id_table.get(id, None) is not None
            ],
        )

    async def get_interpretations_by_name(
        self,
        name: str,
        skip: int = 0,
        limit: int = 100,
        is_desc: bool = False,
    ) -> List[Tag]:
        tokens = await CrudTagToken.get_rows_by_name_order_by_id(
            name, skip=skip, limit=limit, is_desc=is_desc
        )
        tags = []
        for token in tokens:
            tag = await self.get_interpretation_by_id(token.id)
            if tag is None:
                tag = Tag(id=token.id, name=token.name)

            tags.append(tag)
        return tags

    async def update(self, tag: TagUpdate) -> TagInserted:
        return await self.insert(tag)

    async def delete_related_elasticsearch_docs(self, tag_id: int):
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
        batches = []

        async for doc in async_scan(
            client=self.async_elasticsearch, query=query, index=self.index
        ):
            hits = SearchResult(**doc)
            for hit in hits.hits.hits:
                tag = TagElasticsearch(**hit.source)
                try:
                    tag.category_ids.remove(tag_id)
                except ValueError:
                    pass
                try:
                    tag.synonym_ids.remove(tag_id)
                except ValueError:
                    pass
                if tag.representative_id == tag_id:
                    tag.representative_id = None
                action = {
                    "_index": self.index,
                    "_id": tag.id,
                    "_source": tag.model_dump(),
                }
                batches.append(action)
                if len(batches) > self.batch_size:
                    await async_bulk(self.async_elasticsearch, batches)
                    batches = []
        if len(batches) > 0:
            await async_bulk(self.async_elasticsearch, batches)

    async def delete_by_id(self, tag_id: int) -> bool:
        async with async_session() as session:
            async with session.begin():
                await session.execute(
                    delete(TagTokenBase).where(TagTokenBase.id == tag_id)
                )
        await self.delete_related_elasticsearch_docs(tag_id)
        try:
            await self.async_elasticsearch.delete(index=self.index, id=tag_id)
        except NotFoundError:
            pass
        return True
