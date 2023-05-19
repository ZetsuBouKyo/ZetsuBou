import json
import re
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.db.crud import CrudMinioStorage
from back.db.model import StorageMinio
from back.model.base import Protocol, SourceBaseModel
from back.model.elastic import AnalyzerEnum, QueryBoolean
from back.model.gallery import Galleries, Gallery, GalleryOrderedFieldEnum
from back.session.async_elasticsearch import async_elasticsearch
from back.session.storage import get_storage_session_by_source
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from back.utils.dt import (
    get_isoformat_with_timezone,
    get_now,
    is_isoformat_with_timezone,
)
from back.utils.fs import is_image
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk, async_scan
from fastapi import HTTPException

ELASTICSEARCH_INDEX_MAX_RESULT_WINDOW = 10000
ELASTICSEARCH_INDEX_GALLERY = setting.elastic_index_gallery
ELASTICSEARCH_SIZE = setting.elastic_size

BATCH_SIZE = 300

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname


def convert(text) -> int:
    return int(text) if text.isdigit() else text


def alphanum_sorting(text) -> List[int]:
    return [convert(c) for c in re.split("([0-9]+)", text)]


class CrudAsyncElasticsearchGallery(CrudAsyncElasticsearchBase[Gallery]):
    def __init__(
        self,
        hosts: List[str] = None,
        size: int = None,
        index: str = ELASTICSEARCH_INDEX_GALLERY,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        sorting: List[Any] = [
            "_score",
            {"timestamp": {"order": "desc", "unmapped_type": "long"}},
            {"mtime": {"order": "desc", "unmapped_type": "long"}},
            {"attributes.name.keyword": {"order": "desc"}},
        ],
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
    def fields(self):
        if self.analyzer == AnalyzerEnum.DEFAULT.value:
            return [
                "attributes.name",
                "attributes.raw_name",
                "attributes.uploader",
                "attributes.category",
                "attributes.src",
                "labels",
                "tags.*",
            ]
        elif self.analyzer == AnalyzerEnum.NGRAM.value:
            return [
                "attributes.name.ngram",
                "attributes.raw_name.ngram",
                "attributes.uploader",
                "attributes.category",
                "attributes.src.ngram",
                "labels",
                "tags.*",
            ]
        elif self.analyzer == AnalyzerEnum.STANDARD.value:
            return [
                "attributes.name.standard",
                "attributes.raw_name.standard",
                "attributes.uploader",
                "attributes.category",
                "attributes.src.standard",
                "labels",
                "tags.*",
            ]
        return [
            "attributes.name",
            "attributes.raw_name",
            "attributes.uploader",
            "attributes.category",
            "attributes.src",
            "labels",
            "tags.*",
        ]

    async def get_by_id(self, id: str) -> Gallery:
        return await Gallery(**await self.get_source_by_id(id))

    async def advanced_search(
        self,
        page: int = 1,
        keywords: str = None,
        keywords_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        keywords_fuzziness: int = 0,
        keywords_bool: QueryBoolean = QueryBoolean.SHOULD,
        name: str = None,
        name_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        name_fuzziness: int = 0,
        name_bool: QueryBoolean = QueryBoolean.SHOULD,
        raw_name: str = None,
        raw_name_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        raw_name_fuzziness: int = 0,
        raw_name_bool: QueryBoolean = QueryBoolean.SHOULD,
        src: str = None,
        src_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        src_fuzziness: int = 0,
        src_bool: QueryBoolean = QueryBoolean.SHOULD,
        category: str = None,
        rating_gte: int = None,
        rating_lte: int = None,
        order_by: GalleryOrderedFieldEnum = None,
        is_desc: bool = True,
        labels: List[str] = [],
        tags: Dict[str, List[str]] = {},
    ):
        dsl = {
            "query": {"bool": {"must": [], "should": []}},
            "size": self.size,
            "track_total_hits": True,
        }

        sorting = ["_score"]
        if order_by is None:
            sorting.append({"timestamp": {"order": "desc", "unmapped_type": "long"}})
            sorting.append({"attributes.name.keyword": {"order": "desc"}})
        elif is_desc:
            sorting.append({order_by: {"order": "desc"}})
        else:
            sorting.append({order_by: {"order": "asc"}})

        dsl["sort"] = sorting

        if keywords is not None:
            keywords = keywords.split()
            for keyword in keywords:
                dsl["query"]["bool"][keywords_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": keyword,
                                    "fuzziness": keywords_fuzziness,
                                    "fields": self.fields,
                                    "analyzer": keywords_analyzer,
                                }
                            }
                        }
                    }
                )
        if name is not None:
            name_field = "attributes.name"
            if name_analyzer == AnalyzerEnum.DEFAULT.value:
                name_field = "attributes.name"
            elif name_analyzer == AnalyzerEnum.NGRAM.value:
                name_field = "attributes.name.ngram"
            elif name_analyzer == AnalyzerEnum.STANDARD.value:
                name_field = "attributes.name.standard"
            name = name.split()
            for n in name:
                dsl["query"]["bool"][name_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": n,
                                    "fuzziness": name_fuzziness,
                                    "fields": [name_field],
                                    "analyzer": name_analyzer,
                                }
                            }
                        }
                    }
                )

        if raw_name is not None:
            raw_name_field = "attributes.raw_name"
            if raw_name_analyzer == AnalyzerEnum.DEFAULT.value:
                raw_name_field = "attributes.raw_name"
            elif raw_name_analyzer == AnalyzerEnum.NGRAM.value:
                raw_name_field = "attributes.raw_name.ngram"
            elif raw_name_analyzer == AnalyzerEnum.STANDARD.value:
                raw_name_field = "attributes.raw_name.standard"
            raw_name = raw_name.split()
            for n in raw_name:
                dsl["query"]["bool"][raw_name_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": n,
                                    "fuzziness": raw_name_fuzziness,
                                    "fields": [raw_name_field],
                                    "analyzer": raw_name_analyzer,
                                }
                            }
                        }
                    }
                )

        if src is not None:
            src_field = "attributes.src"
            if src_analyzer == AnalyzerEnum.DEFAULT.value:
                src_field = "attributes.src"
            elif src_analyzer == AnalyzerEnum.NGRAM.value:
                src_field = "attributes.src.ngram"
            elif src_analyzer == AnalyzerEnum.STANDARD.value:
                src_field = "attributes.src.standard"
            src = src.split()
            for n in src:
                dsl["query"]["bool"][src_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": n,
                                    "fuzziness": src_fuzziness,
                                    "fields": [src_field],
                                    "analyzer": src_analyzer,
                                }
                            }
                        }
                    }
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


async def get_gallery_by_gallery_id(id: str) -> Gallery:
    crud = CrudAsyncElasticsearchGallery(is_from_setting_if_none=True)
    return await crud.get_by_id(id)


def _get_tag_source(
    storage_session: AsyncS3Session,
    source: SourceBaseModel,
    dir_fname: str,
    tag_fname: str,
) -> SourceBaseModel:
    relative_path = dir_fname + "/" + tag_fname
    return storage_session.get_joined_source(source, relative_path)


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
            "group": "",
            "timestamp": now,
            "mtime": now,
            "attributes": {"name": Path(source.path).name},
        }
    )

    await storage_session.put_json(tag_source, gallery.dict())

    return gallery


async def _get_gallery_tag_from_storage(
    storage_session: AsyncS3Session,
    tag_source: SourceBaseModel,
) -> Gallery:
    response = await storage_session.get_object(tag_source)
    tag = json.loads(response)
    tag = Gallery(**tag)
    return tag


async def _put_gallery_tag_in_storage(
    storage_session: AsyncS3Session,
    gallery: Gallery,
    tag_source: SourceBaseModel,
) -> Gallery:
    await storage_session.put_json(tag_source, gallery.dict())
    return gallery


class CrudAsyncGallery:
    def __init__(
        self,
        gallery_id: str,
        hosts: List[str] = None,
        index: str = None,
        dir_fname: str = None,
        tag_fname: str = None,
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
                self.async_elasticsearch = async_elasticsearch
            if self.index is None:
                self.index = ELASTICSEARCH_INDEX_GALLERY
            if dir_fname is None:
                self.dir_fname = DIR_FNAME
            if tag_fname is None:
                self.tag_fname = TAG_FNAME

    async def init(self):
        self.gallery = await get_gallery_by_gallery_id(self.gallery_id)
        self.storage_session = await get_storage_session_by_source(self.gallery)

    def get_tag_source(self, gallery: Gallery) -> SourceBaseModel:
        return _get_tag_source(
            self.storage_session, gallery, self.dir_fname, self.tag_fname
        )

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

            if not is_isoformat_with_timezone(new_gallery.mtime):
                new_gallery.mtime = get_isoformat_with_timezone(new_gallery.mtime)

            new_gallery.timestamp = get_now()
            new_gallery.labels.sort()
            for key in new_gallery.tags.keys():
                new_gallery.tags[key].sort()

            new_gallery_tag_source = self.get_tag_source(new_gallery)
            new_gallery = await _put_gallery_tag_in_storage(
                self.storage_session, new_gallery, new_gallery_tag_source
            )

            await self.async_elasticsearch.index(
                index=self.index, id=new_gallery.id, body=new_gallery.dict()
            )

            return new_gallery

    async def get_gallery_tag_from_storage(self) -> Gallery:
        tag_source = self.get_tag_source(self.gallery)
        async with self.storage_session:
            tag = await _get_gallery_tag_from_storage(self.storage_session, tag_source)
        return tag

    async def get_image_filenames(self) -> List[str]:
        async with self.storage_session:
            filenames = await self.storage_session.list_filenames(self.gallery)

        images = [filename for filename in filenames if is_image(Path(filename))]
        images.sort(key=alphanum_sorting)
        return images

    async def get_cover(self) -> str:
        images = await self.get_image_filenames()
        if len(images) == 0:
            raise HTTPException(status_code=404, detail="Cover not found")
        cover_filename = images[0]
        return await self.get_image(cover_filename)

    async def get_image(self, image_name: str) -> str:
        async with self.storage_session:
            image_source = self.storage_session.get_joined_source(
                self.gallery, image_name
            )
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


async def get_crud_async_gallery(gallery_id: str) -> CrudAsyncGallery:
    crud = CrudAsyncGallery(gallery_id, is_from_setting_if_none=True)
    await crud.init()
    return crud


class CrudAsyncGallerySync:
    def __init__(
        self,
        storage_session: AsyncS3Session,
        root_source: SourceBaseModel,
        depth: int,
        hosts: List[str] = None,
        index: str = None,
        size: int = None,
        batch_size: int = None,
        dir_fname: str = None,
        tag_fname: str = None,
        is_from_setting_if_none: bool = False,
    ):

        self.storage_session = storage_session

        self.root_source = root_source
        self.depth = depth

        self.hosts = hosts
        self.index = index
        self.size = size
        self.batch_size = batch_size
        self.dir_fname = dir_fname
        self.tag_fname = tag_fname

        self.async_elasticsearch = AsyncElasticsearch(self.hosts)

        if is_from_setting_if_none:
            if self.hosts is None:
                self.async_elasticsearch = async_elasticsearch
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

        self.cache = set()
        self._elasticsearch_to_storage_batches = []
        self._storage_to_elasticsearch_batches = []

    async def iter_elasticsearch_batches(self, batches: List[dict]):
        for batch in batches:
            yield batch

    async def send_bulk(self, batches: List[dict]):
        await async_bulk(self.async_elasticsearch, batches)
        self._elasticsearch_to_storage_batches = []
        self._storage_to_elasticsearch_batches = []

    async def _sync_gallery(self, source: SourceBaseModel) -> Gallery:
        tag_source = _get_tag_source(
            self.storage_session, source, self.dir_fname, self.tag_fname
        )
        if not await self.storage_session.exists(tag_source):
            tag = await _create_gallery_tag_in_storage(
                self.storage_session, source, tag_source
            )

        else:
            tag = await _get_gallery_tag_from_storage(self.storage_session, tag_source)

        now = get_now()

        need_to_update = False
        if not tag.timestamp:
            need_to_update = True
            tag.timestamp = now
        if not tag.mtime:
            need_to_update = True
            tag.mtime = now

        if not is_isoformat_with_timezone(tag.timestamp):
            need_to_update = True
            tag.timestamp = get_isoformat_with_timezone(tag.timestamp)
        if not is_isoformat_with_timezone(tag.mtime):
            need_to_update = True
            tag.mtime = get_isoformat_with_timezone(tag.mtime)

        if not tag.id:
            need_to_update = True
            tag.id = str(uuid4())

        if source.path != tag.path:
            need_to_update = True
            tag.path = source.path

        if need_to_update:
            await _put_gallery_tag_in_storage(self.storage_session, tag, tag_source)

        action = {"_index": self.index, "_id": tag.id, "_source": tag.dict()}
        self._storage_to_elasticsearch_batches.append(action)

        self.cache.add(tag.id)

        if len(self._storage_to_elasticsearch_batches) > self.batch_size:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

        return tag

    async def _sync_storage_to_elasticsearch(self):
        self._storage_to_elasticsearch_batches = []
        async for source in self.storage_session.iter(self.root_source, self.depth):
            if source is None:
                continue

            await self._sync_gallery(source)

        if len(self._storage_to_elasticsearch_batches) > 0:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

    async def _sync_elasticsearch_to_storage_batch(self, galleries: Galleries):
        for hit in galleries.hits.hits:
            if hit.source._scheme != self.root_source._scheme:
                continue

            if not isinstance(hit.source, Gallery):
                source = Gallery(**hit.source.dict())
            else:
                source = hit.source

            exists = await self.storage_session.exists(source)
            if not exists or hit.id not in self.cache:
                self._elasticsearch_to_storage_batches.append(
                    {
                        "_index": self.index,
                        "_id": hit.id,
                        "_op_type": "delete",
                    }
                )

            if len(self._elasticsearch_to_storage_batches) > self.batch_size:
                await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def _sync_elasticsearch_to_storage(self):
        query = {"query": {"match_all": {}}}
        c = 0

        async for doc in async_scan(
            client=self.async_elasticsearch, query=query, index=self.index
        ):
            source = doc.get("_source", None)
            if source is None:
                continue
            c += 1
            gallery = Gallery(**source)

            if gallery._scheme != self.root_source._scheme:
                continue

            exists = await self.storage_session.exists(gallery)
            if not exists or gallery.id not in self.cache:
                self._elasticsearch_to_storage_batches.append(
                    {
                        "_index": self.index,
                        "_id": gallery.id,
                        "_op_type": "delete",
                    }
                )

            if len(self._elasticsearch_to_storage_batches) > self.batch_size:
                await self.send_bulk(self._elasticsearch_to_storage_batches)

        if len(self._elasticsearch_to_storage_batches) > 0:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def sync(self):
        import time

        async with self.storage_session:
            t1 = time.time()
            await self._sync_storage_to_elasticsearch()
            t2 = time.time()
            print(t2 - t1)
            await self._sync_elasticsearch_to_storage()
            t3 = time.time()
            print(t3 - t2)


def get_root_source_by_storage_minio(storage_minio: StorageMinio) -> SourceBaseModel:
    bucket_name = storage_minio.bucket_name
    if bucket_name.endswith("/"):
        bucket_name = bucket_name[:-1]
    prefix = storage_minio.prefix
    if prefix.startswith("/"):
        prefix = prefix[1:]

    root_path = f"{Protocol.MINIO.value}-{storage_minio.id}://{bucket_name}/{prefix}"
    return SourceBaseModel(path=root_path)


async def get_crud_sync_gallery(
    protocol: Protocol, storage_id: int
) -> CrudAsyncGallerySync:
    if protocol == Protocol.MINIO.value:
        storage_minio = await CrudMinioStorage.get_row_by_id(storage_id)
        if storage_minio is None:
            raise HTTPException(
                status_code=404,
                detail=f"Storage MinIO ID: {storage_id} not found",
            )

        storage_session = AsyncS3Session(
            aws_access_key_id=storage_minio.access_key,
            aws_secret_access_key=storage_minio.secret_key,
            endpoint_url=storage_minio.endpoint,
        )

        root_source = get_root_source_by_storage_minio(storage_minio)

        return CrudAsyncGallerySync(
            storage_session,
            root_source,
            storage_minio.depth,
            is_from_setting_if_none=True,
        )
