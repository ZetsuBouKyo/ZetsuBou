from pathlib import Path
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk, async_scan
from fastapi import HTTPException

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.crud.async_progress import Progress
from back.db.crud import CrudStorageMinio
from back.init.check import ping_elasticsearch, ping_storage
from back.logging import logger_zetsubou
from back.model.base import SourceBaseModel, SourceProtocolEnum
from back.model.elasticsearch import (
    ElasticsearchAnalyzerEnum,
    ElasticsearchCleanResult,
    ElasticsearchKeywordAnalyzers,
    ElasticsearchQueryBooleanEnum,
)
from back.model.gallery import Galleries, Gallery, GalleryOrderedFieldEnum
from back.model.task import ZetsuBouTaskProgressEnum
from back.session.async_elasticsearch import get_async_elasticsearch
from back.session.storage import get_storage_session_by_source
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from back.utils.dt import (
    get_isoformat_with_timezone,
    get_now,
    is_isoformat_with_timezone,
)
from back.utils.session import AsyncSession, session

ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW = 10000
ELASTICSEARCH_INDEX_GALLERY = setting.elastic_index_gallery
ELASTICSEARCH_SIZE = setting.elastic_size
ELASTICSEARCH_DELETE_REDUNDANT_DOCS = setting.elasticsearch_delete_redundant_docs

BATCH_SIZE = 300

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname

APP_GALLERY_SYNC_PAGES = setting.app_gallery_sync_pages

elasticsearch_gallery_analyzer: ElasticsearchKeywordAnalyzers = {
    ElasticsearchAnalyzerEnum.DEFAULT.value: [
        "path.url",
        "name.default",
        "raw_name.default",
        "other_names.default",
        "src.url",
        "attributes.category",
        "attributes.uploader",
        "labels",
        "tags.*",
    ],
    ElasticsearchAnalyzerEnum.KEYWORD.value: [
        "path.keyword",
        "name.keyword",
        "raw_name.keyword",
        "other_names.keyword",
        "src.keyword",
        "attributes.category",
        "attributes.uploader",
        "labels",
        "tags.*",
    ],
    ElasticsearchAnalyzerEnum.NGRAM.value: [
        "path.ngram",
        "name.ngram",
        "raw_name.ngram",
        "other_names.ngram",
        "src.ngram",
        "attributes.category",
        "attributes.uploader",
        "labels",
        "tags.*",
    ],
    ElasticsearchAnalyzerEnum.STANDARD.value: [
        "path.standard",
        "name.standard",
        "raw_name.standard",
        "other_names.standard",
        "src.standard",
        "attributes.category",
        "attributes.uploader",
        "labels",
        "tags.*",
    ],
    ElasticsearchAnalyzerEnum.URL.value: ["path.url", "src.url"],
}


def get_sync_gallery_progress_id(protocol: SourceProtocolEnum, id: int):
    return f"{ZetsuBouTaskProgressEnum.SYNC_STORAGE}.{protocol}.{id}"


class CrudAsyncElasticsearchGallery(CrudAsyncElasticsearchBase[Gallery]):
    def __init__(
        self,
        hosts: Optional[List[str]] = None,
        index: str = ELASTICSEARCH_INDEX_GALLERY,
        keyword_analyzers: ElasticsearchKeywordAnalyzers = elasticsearch_gallery_analyzer,
        sorting: List[Any] = [
            "_score",
            {"last_updated": {"order": "desc", "unmapped_type": "long"}},
            {"upload_date": {"order": "desc", "unmapped_type": "long"}},
            {"name.keyword": {"order": "desc"}},
        ],
        is_from_setting_if_none: bool = False,
    ):
        super().__init__(
            hosts=hosts,
            index=index,
            keyword_analyzers=keyword_analyzers,
            sorting=sorting,
            is_from_setting_if_none=is_from_setting_if_none,
        )

    @session
    async def get_by_id(self, id: str) -> Gallery:
        return Gallery(**await self.get_source_by_id(id))

    @session
    async def advanced_search(
        self,
        page: int = 1,
        size: int = ELASTICSEARCH_SIZE,
        keywords: Optional[str] = None,
        keywords_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        keywords_fuzziness: int = 0,
        keywords_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        name: Optional[str] = None,
        name_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        name_fuzziness: int = 0,
        name_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        raw_name: Optional[str] = None,
        raw_name_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        raw_name_fuzziness: int = 0,
        raw_name_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        other_names: Optional[str] = None,
        other_names_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.DEFAULT,
        other_names_fuzziness: int = 0,
        other_names_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        src: Optional[str] = None,
        src_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.URL,
        src_fuzziness: int = 0,
        src_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        path: Optional[str] = None,
        path_analyzer: ElasticsearchAnalyzerEnum = ElasticsearchAnalyzerEnum.URL,
        path_fuzziness: int = 0,
        path_bool: ElasticsearchQueryBooleanEnum = ElasticsearchQueryBooleanEnum.SHOULD,
        category: Optional[str] = None,
        uploader: Optional[str] = None,
        rating_gte: Optional[int] = None,
        rating_lte: Optional[int] = None,
        order_by: Optional[GalleryOrderedFieldEnum] = None,
        is_desc: bool = True,
        labels: List[str] = [],
        tags: Dict[str, List[str]] = {},
    ):
        dsl = {
            "query": {"bool": {"must": [], "should": []}},
            "size": size,
            "track_total_hits": True,
        }

        sorting = ["_score"]
        if order_by is None:
            sorting.append({"last_updated": {"order": "desc", "unmapped_type": "long"}})
            sorting.append({"name.keyword": {"order": "desc"}})
        elif is_desc:
            sorting.append({order_by: {"order": "desc"}})
        else:
            sorting.append({order_by: {"order": "asc"}})

        dsl["sort"] = sorting

        if keywords is not None:
            if type(keywords_bool) is not str:
                keywords_bool = keywords_bool.value

            keywords = keywords.split()
            keyword_fields = self.get_keyword_fields(keywords_analyzer)
            for keyword in keywords:
                dsl["query"]["bool"][keywords_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": keyword,
                                    "fuzziness": keywords_fuzziness,
                                    "fields": keyword_fields,
                                }
                            }
                        }
                    }
                )
        if name is not None:
            self.add_advanced_query(
                dsl, name, "name", name_analyzer, name_fuzziness, name_bool
            )

        if raw_name is not None:
            self.add_advanced_query(
                dsl,
                raw_name,
                "raw_name",
                raw_name_analyzer,
                raw_name_fuzziness,
                raw_name_bool,
            )

        if other_names is not None:
            self.add_advanced_query(
                dsl,
                other_names,
                "other_names",
                other_names_analyzer,
                other_names_fuzziness,
                other_names_bool,
            )

        if src is not None:
            self.add_advanced_query(
                dsl,
                src,
                "src",
                src_analyzer,
                src_fuzziness,
                src_bool,
            )

        if path is not None:
            self.add_advanced_query(
                dsl,
                path,
                "path",
                path_analyzer,
                path_fuzziness,
                path_bool,
            )

        if category is not None:
            dsl["query"]["bool"]["must"].append(
                {
                    "constant_score": {
                        "filter": {
                            "multi_match": {
                                "query": category,
                                "fields": ["attributes.category"],
                            }
                        }
                    }
                }
            )

        if uploader is not None:
            dsl["query"]["bool"]["must"].append(
                {
                    "constant_score": {
                        "filter": {
                            "multi_match": {
                                "query": uploader,
                                "fields": ["attributes.uploader"],
                            }
                        }
                    }
                }
            )

        if rating_gte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.rating": {"gte": rating_gte}}}
            )
        if rating_lte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.rating": {"lte": rating_lte}}}
            )

        for label in labels:
            dsl["query"]["bool"]["must"].append(
                {
                    "constant_score": {
                        "filter": {
                            "multi_match": {
                                "query": label,
                                "fields": ["labels"],
                            }
                        }
                    }
                }
            )

        for tag_field, tag_values in tags.items():
            for tag_value in tag_values:
                dsl["query"]["bool"]["must"].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": tag_value,
                                    "fields": [f"tags.{tag_field}"],
                                }
                            }
                        }
                    }
                )

        return await self.query(page, dsl)

    @session
    async def match_phrase_prefix(
        self, keywords: str, size: int = ELASTICSEARCH_SIZE
    ) -> Galleries:
        query = {
            "bool": {
                "should": [
                    {"match_phrase_prefix": {"name.ngram": {"query": keywords}}},
                    {"match_phrase_prefix": {"raw_name.ngram": {"query": keywords}}},
                ]
            }
        }
        _resp = await self.async_elasticsearch.search(
            index=self.index, query=query, size=size
        )
        sources = Galleries(**_resp)
        return sources


async def get_gallery_by_gallery_id(id: str) -> Gallery:
    async with CrudAsyncElasticsearchGallery(is_from_setting_if_none=True) as crud:
        doc = await crud.get_by_id(id)
    return doc


async def _create_gallery_tag_in_storage(
    storage_session: AsyncS3Session,
    source: SourceBaseModel,
    tag_source: SourceBaseModel,
) -> Gallery:
    now = get_now()
    gallery = Gallery(
        **{
            "id": str(uuid4()),
            "path": source.path,
            "name": Path(source.path).name,
            "last_updated": now,
            "upload_date": now,
        }
    )

    await storage_session.put_json(tag_source, gallery.model_dump())

    return gallery


async def _get_gallery_tag_from_storage(
    storage_session: AsyncS3Session,
    tag_source: SourceBaseModel,
) -> Gallery:
    tag_dict = await storage_session.get_json(tag_source)
    tag = Gallery(**tag_dict)
    return tag


async def _put_gallery_tag_in_storage(
    storage_session: AsyncS3Session,
    gallery: Gallery,
    tag_source: SourceBaseModel,
) -> Gallery:
    await storage_session.put_json(tag_source, gallery.model_dump())
    return gallery


class CrudAsyncGallery:
    def __init__(
        self,
        gallery_id: str,
        hosts: Optional[List[str]] = None,
        index: Optional[str] = None,
        dir_fname: Optional[str] = None,
        tag_fname: Optional[str] = None,
        is_from_setting_if_none: bool = False,
    ):
        self.gallery_id = gallery_id
        self.hosts = hosts
        self.async_elasticsearch = AsyncElasticsearch(self.hosts)
        self.index = index
        self.dir_fname = dir_fname
        self.tag_fname = tag_fname
        self.storage_session = None

        if is_from_setting_if_none:
            if self.hosts is None:
                self.async_elasticsearch = get_async_elasticsearch()
            if self.index is None:
                self.index = ELASTICSEARCH_INDEX_GALLERY
            if dir_fname is None:
                self.dir_fname = DIR_FNAME
            if tag_fname is None:
                self.tag_fname = TAG_FNAME

    async def init(self):
        self.gallery = await get_gallery_by_gallery_id(self.gallery_id)
        self.storage_session = await get_storage_session_by_source(self.gallery)

    async def close(self):
        await self.async_elasticsearch.close()

    async def __aenter__(self):
        await self.init()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.close()

    def get_tag_source(self, gallery: Gallery) -> SourceBaseModel:
        return gallery.get_joined_source(self.dir_fname, self.tag_fname)

    async def update(self, new_gallery: Gallery) -> Gallery:
        async with self.storage_session:
            old_gallery = self.gallery

            if new_gallery.id != old_gallery.id:
                raise HTTPException(
                    status_code=409,
                    detail="Conflict between elastic gallery and new gallery ID",
                )

            if new_gallery.path != old_gallery.path:
                raise HTTPException(
                    status_code=409,
                    detail="Conflict between elastic gallery and new gallery path",
                )

            if not await self.storage_session.exists(old_gallery):
                raise HTTPException(
                    status_code=404, detail=f"Gallery ID: {self.gallery.id} not found"
                )

            old_gallery_tag_source = self.get_tag_source(old_gallery)
            old_gallery_from_storage = await _get_gallery_tag_from_storage(
                self.storage_session, old_gallery_tag_source
            )

            if new_gallery.id != old_gallery_from_storage.id:
                raise HTTPException(
                    status_code=409,
                    detail="Conflict between storage gallery and elastic gallery id",
                )

            if new_gallery.path != old_gallery_from_storage.path:
                raise HTTPException(
                    status_code=409,
                    detail="Conflict between minio gallery and elastic gallery path",
                )

            if not is_isoformat_with_timezone(new_gallery.upload_date):
                new_gallery.upload_date = get_isoformat_with_timezone(
                    new_gallery.upload_date
                )

            new_gallery.last_updated = get_now()
            new_gallery.labels.sort()
            for key in new_gallery.tags.keys():
                new_gallery.tags[key].sort()

            new_gallery_tag_source = self.get_tag_source(new_gallery)
            new_gallery = await _put_gallery_tag_in_storage(
                self.storage_session, new_gallery, new_gallery_tag_source
            )

            await self.async_elasticsearch.index(
                index=self.index, id=new_gallery.id, document=new_gallery.model_dump()
            )

            return new_gallery

    async def get_gallery_tag_from_storage(self) -> Gallery:
        tag_source = self.get_tag_source(self.gallery)
        async with self.storage_session:
            tag = await _get_gallery_tag_from_storage(self.storage_session, tag_source)
        return tag

    async def get_image_filenames(self) -> List[str]:
        async with self.storage_session:
            images = await self.storage_session.list_images(self.gallery)

        return images

    async def get_cover(self) -> str:
        images = await self.get_image_filenames()
        if len(images) == 0:
            raise HTTPException(status_code=404, detail="Cover not found")
        cover_filename = images[0]
        return await self.get_image(cover_filename)

    async def get_image(self, image_name: str) -> str:
        async with self.storage_session:
            image_source = self.gallery.get_joined_source(image_name)
            return await self.storage_session.get_url(image_source)

    async def exists(
        self,
    ) -> bool:
        async with self.storage_session:
            return await self.storage_session.exists(self.gallery)

    async def delete(self) -> str:
        async with self.storage_session:
            await self.storage_session.delete(self.gallery)
        await self.async_elasticsearch.delete(index=self.index, id=self.gallery.id)
        return "ok"


class CrudAsyncGallerySync(AsyncSession):

    def __init__(
        self,
        storage_session: AsyncS3Session,
        storage_protocol: SourceProtocolEnum,
        storage_id: int,
        root_source: SourceBaseModel,
        depth: int,
        hosts: Optional[List[str]] = None,
        index: Optional[str] = None,
        target_index: Optional[str] = None,
        size: Optional[int] = None,
        batch_size: Optional[int] = None,
        force: bool = ELASTICSEARCH_DELETE_REDUNDANT_DOCS,
        dir_fname: Optional[str] = None,
        tag_fname: Optional[str] = None,
        progress_id: Optional[str] = None,
        progress_initial: float = 0,
        progress_final: float = 100.0,
        sync_pages: Optional[bool] = None,
        callback: Optional[Callable[[Gallery], SourceBaseModel]] = None,
        new_gallery_model: Optional[SourceBaseModel] = None,
        is_progress: bool = True,
        is_from_setting_if_none: bool = False,
    ):
        self.storage_session = storage_session
        self.storage_protocol = storage_protocol
        self.storage_id = storage_id

        self.root_source = root_source
        self.depth = depth

        self.hosts = hosts
        self.index = index
        self.target_index = target_index  # the target index for synchronization
        self.size = size
        self.batch_size = batch_size
        self.force = force
        self.dir_fname = dir_fname
        self.tag_fname = tag_fname

        self.async_elasticsearch = AsyncElasticsearch(self.hosts)

        self.progress_initial = progress_initial
        self.progress_final = progress_final
        self.progress_interval = self.progress_final - self.progress_initial
        self.progress_id = progress_id
        if self.progress_id is None:
            self.progress_id = get_sync_gallery_progress_id(
                self.storage_protocol, self.storage_id
            )
        self.sync_pages = sync_pages
        self.callback = callback
        self.new_gallery_model = new_gallery_model
        self.is_progress = is_progress

        if is_from_setting_if_none:
            if self.hosts is None:
                self.async_elasticsearch = get_async_elasticsearch()
            if self.index is None:
                self.index = ELASTICSEARCH_INDEX_GALLERY
            if self.size is None:
                self.size = ELASTICSEARCH_SIZE
            if self.batch_size is None:
                self.batch_size = BATCH_SIZE
            if self.dir_fname is None:
                self.dir_fname = DIR_FNAME
            if self.tag_fname is None:
                self.tag_fname = TAG_FNAME
            if self.sync_pages is None:
                self.sync_pages = APP_GALLERY_SYNC_PAGES

        self.cache = set()
        self._elasticsearch_to_storage_batches = []
        self._storage_to_elasticsearch_batches = []

    @property
    def dsl(self):
        return {
            "size": 0,
            "query": {
                "constant_score": {
                    "filter": {
                        "multi_match": {
                            "query": f"{self.storage_protocol}-{self.storage_id}",
                            "fields": [f"path.{ElasticsearchAnalyzerEnum.URL}"],
                        }
                    }
                }
            },
            "track_total_hits": True,
        }

    async def close(self):
        await self.async_elasticsearch.close()

    async def are_galleries(self):
        async with self.storage_session:
            return await self.storage_session.are_galleries(
                self.root_source, self.depth
            )

    async def iter_elasticsearch_batches(self, batches: List[dict]):
        for batch in batches:
            yield batch

    @session
    async def send_bulk(self, batches: List[dict]):
        await async_bulk(self.async_elasticsearch, batches)
        self._elasticsearch_to_storage_batches = []
        self._storage_to_elasticsearch_batches = []

    async def _sync_gallery_storage_to_elasticsearch(
        self, source: SourceBaseModel
    ) -> Gallery:
        """Update the Elasticsearch document based on the stored JSON file without
        checking for differences between the two documents.

        In some cases, we need to update the JSON file in storage as well.
        """

        tag_source = source.get_joined_source(self.dir_fname, self.tag_fname)
        if not await self.storage_session.exists(tag_source):
            tag = await _create_gallery_tag_in_storage(
                self.storage_session, source, tag_source
            )

        else:
            tag = await _get_gallery_tag_from_storage(self.storage_session, tag_source)

        # check if we need to update the JSON file in the storage
        need_to_update = False

        now = get_now()

        if not tag.last_updated:
            need_to_update = True
            tag.last_updated = now
        if not tag.upload_date:
            need_to_update = True
            tag.upload_date = now

        if not is_isoformat_with_timezone(tag.last_updated):
            need_to_update = True
            tag.last_updated = get_isoformat_with_timezone(tag.last_updated)
        if not is_isoformat_with_timezone(tag.upload_date):
            need_to_update = True
            tag.upload_date = get_isoformat_with_timezone(tag.upload_date)

        if not tag.id:
            need_to_update = True
            tag.id = str(uuid4())

        if source.path != tag.path:
            need_to_update = True
            tag.path = source.path

        if self.sync_pages:
            images = await self.storage_session.list_images(source)
            gallery_pages = len(images)
            if gallery_pages != tag.attributes.pages:
                tag.attributes.pages = gallery_pages
                need_to_update = True

        if self.callback is not None:
            tag = self.callback(tag)
            if self.new_gallery_model is None:
                assert isinstance(tag, Gallery)
            else:
                assert isinstance(tag, self.new_gallery_model)
            need_to_update = True

        if need_to_update:
            # update the JSON file in storage
            await _put_gallery_tag_in_storage(self.storage_session, tag, tag_source)

        # add the document to batches to update the document in Elasticsearch
        index = self.index
        if self.target_index is not None:
            index = self.target_index
        action = {"_index": index, "_id": tag.id, "_source": tag.model_dump()}
        self._storage_to_elasticsearch_batches.append(action)

        self.cache.add(tag.id)

        if len(self._storage_to_elasticsearch_batches) > self.batch_size:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

        return tag

    async def _sync_gallery_elasticsearch_to_storage(self, doc: dict):
        source = doc.get("_source", None)
        if source is None:
            return

        gallery = Gallery(**source)

        if gallery._scheme != self.root_source._scheme:
            return

        exists = await self.storage_session.exists(gallery)
        if (not exists or gallery.id not in self.cache) and self.force:
            self._elasticsearch_to_storage_batches.append(
                {
                    "_index": self.index,
                    "_id": gallery.id,
                    "_op_type": "delete",
                }
            )

        if len(self._elasticsearch_to_storage_batches) > self.batch_size:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def _sync_storage_to_elasticsearch_without_progress(self):
        async for source in self.storage_session.iter_directories(
            self.root_source, self.depth
        ):
            if source is None:
                continue

            await self._sync_gallery_storage_to_elasticsearch(source)

        if len(self._storage_to_elasticsearch_batches) > 0:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

    async def _sync_elasticsearch_to_storage_without_progress(self):
        query = self.dsl

        async for doc in async_scan(
            client=self.async_elasticsearch, query=query, index=self.index
        ):
            await self._sync_gallery_elasticsearch_to_storage(doc)

        if len(self._elasticsearch_to_storage_batches) > 0:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def _count_storage(self):
        self._sources = []
        async for source in self.storage_session.iter_directories(
            self.root_source, self.depth
        ):
            if source is None:
                continue
            self._sources.append(source)

        self._storage_to_elasticsearch_num = len(self._sources)

        logger_zetsubou.debug(
            f"storage to elasticsearch (number): {self._storage_to_elasticsearch_num}"
        )

    async def _count_docs(self):
        dsl = self.dsl

        resp = await self.async_elasticsearch.search(index=self.index, **dsl)
        self._elasticsearch_to_storage_num = resp["hits"]["total"]["value"]

        logger_zetsubou.debug(
            f"elasticsearch to storage (number): {self._elasticsearch_to_storage_num}"
        )

    async def _count_to_docs(self):
        """Count the number of documents in the `self.target_index` index."""
        if self.target_index is None:
            return
        dsl = self.dsl
        resp = await self.async_elasticsearch.search(index=self.target_index, **dsl)
        total = resp["hits"]["total"]["value"]
        if total > 0:
            raise ValueError(f"Index: {self.target_index} should be empty.")

    async def _sync_storage_to_elasticsearch(self):
        self._storage_to_elasticsearch_final = self.progress_initial + (
            self._storage_to_elasticsearch_num
            / (self._storage_to_elasticsearch_num + self._elasticsearch_to_storage_num)
            * self.progress_interval
        )

        async for source in Progress(
            self._sources,
            id=self.progress_id,
            initial=self.progress_initial,
            final=self._storage_to_elasticsearch_final,
            total=self._storage_to_elasticsearch_num,
            is_from_setting_if_none=True,
        ):
            await self._sync_gallery_storage_to_elasticsearch(source)

        if len(self._storage_to_elasticsearch_batches) > 0:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

    async def _sync_elasticsearch_to_storage(self):
        query = self.dsl

        async for doc in Progress(
            async_scan(client=self.async_elasticsearch, query=query, index=self.index),
            id=self.progress_id,
            initial=self._storage_to_elasticsearch_final,
            final=self.progress_final,
            total=self._elasticsearch_to_storage_num,
            is_from_setting_if_none=True,
        ):
            await self._sync_gallery_elasticsearch_to_storage(doc)

        if len(self._elasticsearch_to_storage_batches) > 0:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    @session
    async def sync(self):
        logger_zetsubou.debug(f"storage protocol: {self.storage_protocol}")
        logger_zetsubou.debug(f"storage id: {self.storage_id}")
        logger_zetsubou.debug(f"elasticsearch index: {self.index}")
        logger_zetsubou.debug(f"is progress: {self.is_progress}")
        logger_zetsubou.debug(f"progress id: {self.progress_id}")

        is_elasticsearch = await ping_elasticsearch()
        is_storage = await ping_storage()
        if not is_elasticsearch or not is_storage:
            return

        async with self.storage_session:
            await self._count_to_docs()
            if self.is_progress:
                await self._count_docs()
                await self._count_storage()

                await self._sync_storage_to_elasticsearch()
                await self._sync_elasticsearch_to_storage()
            else:
                await self._sync_storage_to_elasticsearch_without_progress()
                await self._sync_elasticsearch_to_storage_without_progress()


async def clean_elasticsearch_gallery(
    async_elasticsearch: AsyncElasticsearch,
    index: str = ELASTICSEARCH_INDEX_GALLERY,
    batch_size: int = BATCH_SIZE,
) -> ElasticsearchCleanResult:
    """
    Remove Elasticsearch gallery documents that no longer exist in the database storage table.

    Caution: If `ZETSUBOU_GALLERY_DIR_FNAME` is not set, consider adding a new environment variable here to confirm the
    removal of documents.
    """
    results = ElasticsearchCleanResult()
    batches = []
    dsl = {
        "query": {
            "bool": {
                "must": {"match_all": {}},
                "must_not": [],
            }
        },
        "track_total_hits": True,
    }
    storages = await CrudStorageMinio.get_all_rows_order_by_id()
    for storage in storages:
        storage_id = storage["id"]
        q = {
            "constant_score": {
                "filter": {
                    "multi_match": {
                        "query": f"{SourceProtocolEnum.MINIO.value}-{storage_id}",
                        "fields": [f"path.{ElasticsearchAnalyzerEnum.URL}"],
                    }
                }
            }
        }
        dsl["query"]["bool"]["must_not"].append(q)

    async for doc in async_scan(client=async_elasticsearch, query=dsl, index=index):
        source = doc.get("_source", None)
        gallery = Gallery(**source)
        results.storage[gallery._scheme] += 1
        batches.append(
            {
                "_index": index,
                "_id": gallery.id,
                "_op_type": "delete",
            }
        )
        if len(batches) >= batch_size:
            await async_bulk(async_elasticsearch, batches)
            results.total += len(batches)
            batches = []
    if len(batches) > 0:
        results.total += len(batches)
        await async_bulk(async_elasticsearch, batches)
        batches = []

    return results
