import json
import re
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.crud.elastic import CrudElasticBase, get_source_by_id
from back.crud.minio import CrudMinio, get_minio_client_by_source
from back.db.crud import CrudMinioStorage
from back.db.model import MinioStorage, StorageMinio
from back.model.base import Protocol, SourceBaseModel
from back.model.elastic import AnalyzerEnum, QueryBoolean
from back.model.gallery import Galleries, Gallery, GalleryOrderedFieldEnum
from back.session.async_elasticsearch import async_elasticsearch
from back.session.elastic import elastic_client
from back.session.minio import get_minio_client
from back.session.storage import get_storage_session_by_source
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from back.utils.dt import (
    get_isoformat_with_timezone,
    get_now,
    is_isoformat_with_timezone,
)
from back.utils.fs import is_image
from elasticsearch import AsyncElasticsearch, Elasticsearch, helpers
from elasticsearch.helpers import async_bulk, async_scan
from fastapi import HTTPException

from minio import Minio
from minio.error import S3Error

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
    source = await crud.get_source_by_id(id)
    return Gallery(**source)


class CrudElasticGallery(CrudElasticBase[Gallery]):
    def __init__(
        self,
        elastic_client: Elasticsearch = elastic_client,
        size: int = ELASTICSEARCH_SIZE,
        index: str = ELASTICSEARCH_INDEX_GALLERY,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
    ):
        super().__init__(
            elastic_client=elastic_client,
            size=size,
            index=index,
            analyzer=analyzer,
            sorting=[
                "_score",
                {"timestamp": {"order": "desc", "unmapped_type": "long"}},
                {"mtime": {"order": "desc", "unmapped_type": "long"}},
                {"attributes.name.keyword": {"order": "desc"}},
            ],
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

    def advanced_search(
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

        return self.query(page, dsl)


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


class CrudAsyncStorageGallery:
    def __init__(
        self,
        storage_session: AsyncS3Session,
        dir_fname: str = None,
        tag_fname: str = None,
        is_from_setting_if_none: bool = False,
    ):
        self.storage_session = storage_session

        if is_from_setting_if_none:
            if dir_fname is None:
                self.dir_fname = DIR_FNAME
            if tag_fname is None:
                self.tag_fname = TAG_FNAME

    def get_tag_source(self, gallery: Gallery) -> SourceBaseModel:
        return _get_tag_source(
            self.storage_session, gallery, self.dir_fname, self.tag_fname
        )

    async def create_gallery_tag(self, source: SourceBaseModel) -> Gallery:
        tag_source = self.get_tag_source(source)
        async with self.storage_session:
            gallery = await _create_gallery_tag_in_storage(
                self.storage_session, source, tag_source
            )

        return gallery

    async def get_gallery_tag(self, gallery: Gallery) -> Gallery:
        tag_source = self.get_tag_source(gallery)
        async with self.storage_session:
            tag = await _get_gallery_tag_from_storage(self.storage_session, tag_source)
        return tag

    async def put_gallery_tag(self, gallery: Gallery) -> Gallery:
        tag_source = self.get_tag_source(gallery)
        async with self.storage_session:
            gallery = await _put_gallery_tag_in_storage(
                self.storage_session, gallery, tag_source
            )
        return gallery

    async def get_image_filenames(self, gallery: Gallery) -> List[str]:
        async with self.storage_session:
            filenames = await self.storage_session.list_filenames(gallery)

        images = [filename for filename in filenames if is_image(Path(filename))]
        images.sort(key=alphanum_sorting)
        return images

    async def get_cover(self, gallery: Gallery) -> str:
        images = await self.get_image_filenames(gallery)
        if len(images) == 0:
            raise HTTPException(status_code=404, detail="Cover not found")
        cover_filename = images[0]
        return await self.get_image(gallery, cover_filename)

    async def get_image(self, gallery: Gallery, image_name: str) -> str:
        async with self.storage_session:
            image_source = self.storage_session.get_joined_source(gallery, image_name)
            return await self.storage_session.get_url(image_source)

    async def exists(self, gallery: Gallery) -> bool:
        async with self.storage_session:
            return await self.storage_session.exists(gallery)

    async def delete(self, gallery: Gallery) -> str:
        async with self.storage_session:
            return await self.storage_session.delete(gallery)


async def get_crud_async_storage_gallery_by_gallery(
    gallery: Gallery,
) -> CrudAsyncStorageGallery:
    storage_session = await get_storage_session_by_source(gallery)
    return CrudAsyncStorageGallery(
        storage_session=storage_session, is_from_setting_if_none=True
    )


# TODO: deprecated
class CrudMinioGallery(CrudMinio):
    def __init__(
        self, *args, dir_fname: str = DIR_FNAME, tag_fname: str = TAG_FNAME, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.dir_fname = dir_fname
        self.tag_fname = tag_fname

    def tag_object_name(self, object_name: str):
        return f"{object_name}{self.dir_fname}/{self.tag_fname}"

    def create_tag_in_gallery(
        self, bucket_name: str, object_name: str, minio_path: str
    ) -> Gallery:
        now = get_now()
        gallery = Gallery(
            **{
                "id": str(uuid4()),
                "path": minio_path,
                "group": "",
                "timestamp": now,
                "mtime": now,
                "attributes": {"name": Path(minio_path).name},
            }
        )
        tag_object_name = self.tag_object_name(object_name)

        self.put_json(bucket_name, tag_object_name, gallery.dict())

        return gallery

    def get_tag(self, bucket_name: str, tag_object_name: str) -> Gallery:
        response = self.minio_client.get_object(bucket_name, tag_object_name)
        tag = json.load(response)
        tag = Gallery(**tag)
        response.close()
        response.release_conn()
        return tag

    def get_tag_by_gallery(self, gallery: Gallery):
        tag_object_name = self.tag_object_name(gallery.object_name)
        return self.get_tag(gallery.bucket_name, tag_object_name)

    def put_tag(self, gallery: Gallery):
        bucket_name = gallery.bucket_name
        object_name = gallery.object_name
        tag_object_name = self.tag_object_name(object_name)

        self.put_json(bucket_name, tag_object_name, gallery.dict())

    def get_sorted_image_file_names(self, gallery: Gallery) -> List[str]:
        bucket_name = gallery.bucket_name
        object_name = gallery.object_name
        objs = self.list(bucket_name, object_name, limit=None)
        images = [
            Path(obj.object_name).name
            for obj in objs
            if is_image(Path(obj.object_name))
        ]
        images.sort(key=alphanum_sorting)
        return images

    def get_cover(self, gallery: Gallery) -> str:
        images = self.get_sorted_image_file_names(gallery)
        if len(images) == 0:
            raise HTTPException(status_code=404, detail="Cover not found")
        return images[0]


# TODO: deprecated
def get_gallery_by_id(
    gallery_id: str,
    elastic_client: Elasticsearch = elastic_client,
    index: str = ELASTICSEARCH_INDEX_GALLERY,
) -> Gallery:
    return get_source_by_id(
        gallery_id, Gallery, elastic_client=elastic_client, index=index
    )


class CrudAsyncGallery:
    def __init__(
        self,
        gallery_id: str,
        hosts: List[str] = None,
        index: str = None,
        is_from_setting_if_none: bool = False,
    ):
        self.gallery_id = gallery_id
        self.async_elasticsearch = AsyncElasticsearch(hosts)
        self.index = index
        if is_from_setting_if_none:
            if hosts is None:
                self.async_elasticsearch = async_elasticsearch
            if index is None:
                self.index = ELASTICSEARCH_INDEX_GALLERY

    async def init(self):
        self.gallery = await get_gallery_by_gallery_id(self.gallery_id)
        self.crud_async_storage_gallery = (
            await get_crud_async_storage_gallery_by_gallery(self.gallery)
        )

    async def update(self, new_gallery: Gallery) -> Gallery:
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

        crud_async_storage_gallery = self.crud_async_storage_gallery

        if not await crud_async_storage_gallery.exists(old_gallery):
            raise HTTPException(
                status_code=404, detail=f"Gallery ID: {self.gallery.id} not found"
            )

        old_gallery_from_storage = await crud_async_storage_gallery.get_gallery_tag(
            old_gallery
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

        await crud_async_storage_gallery.put_gallery_tag(new_gallery)
        await self.async_elasticsearch.index(
            index=self.index, id=new_gallery.id, body=new_gallery.dict()
        )

        return new_gallery

    async def get_images(self) -> List[str]:
        return await self.crud_async_storage_gallery.get_image_filenames(self.gallery)

    async def get_cover(self) -> str:
        return await self.crud_async_storage_gallery.get_cover(self.gallery)

    async def get_image(self, image_name: str) -> str:
        return await self.crud_async_storage_gallery.get_image(self.gallery, image_name)

    async def delete(self) -> str:
        await self.async_elasticsearch.delete(index=self.index, id=self.gallery.id)
        await self.crud_async_storage_gallery.delete(self.gallery)
        return "ok"


async def get_crud_async_gallery(gallery_id: str) -> CrudAsyncGallery:
    crud = CrudAsyncGallery(gallery_id, is_from_setting_if_none=True)
    await crud.init()
    return crud


# TODO: deprecated
class CrudGallery:
    def __init__(
        self,
        gallery_id: str,
        elastic_client: Elasticsearch = elastic_client,
        crud_minio_storage: CrudMinioStorage = CrudMinioStorage,
        index: str = ELASTICSEARCH_INDEX_GALLERY,
    ):
        self.gallery = get_gallery_by_id(
            gallery_id, elastic_client=elastic_client, index=index
        )
        self.crud_minio_storage = crud_minio_storage

        self.elastic_client = elastic_client
        self.index = index

    async def init(self):
        minio_client = await get_minio_client_by_source(
            self.gallery, self.crud_minio_storage
        )
        self.crud_minio = CrudMinioGallery(minio_client=minio_client)

    def exists_in_minio(self) -> bool:
        return self.crud_minio.exists(
            self.gallery.bucket_name, self.gallery.object_name
        )

    def update(self, new_gallery: Gallery) -> Gallery:
        if new_gallery.id != self.gallery.id:
            raise HTTPException(
                status_code=409,
                detail="Conflict between elastic gallery and new gallery ids",
            )
        if new_gallery.path != self.gallery.path:
            raise HTTPException(
                status_code=409,
                detail="Conflict between elastic gallery and new gallery paths",
            )

        if not self.exists_in_minio():
            raise HTTPException(
                status_code=404, detail=f"Gallery id: {self.gallery.id} not found"
            )

        old_gallery_from_minio = self.crud_minio.get_tag_by_gallery(self.gallery)
        if new_gallery.id != old_gallery_from_minio.id:
            raise HTTPException(
                status_code=409,
                detail="Conflict between minio gallery and elastic gallery ids",
            )
        if new_gallery.path != old_gallery_from_minio.path:
            raise HTTPException(
                status_code=409,
                detail="Conflict between minio gallery and elastic gallery paths",
            )

        if not is_isoformat_with_timezone(new_gallery.mtime):
            new_gallery.mtime = get_isoformat_with_timezone(new_gallery.mtime)

        new_gallery.timestamp = get_now()
        new_gallery.labels.sort()
        for key in new_gallery.tags.keys():
            new_gallery.tags[key].sort()

        self.crud_minio.put_tag(new_gallery)
        self.elastic_client.index(
            index=self.index, id=new_gallery.id, body=new_gallery.dict()
        )

        return new_gallery

    def get_images(self) -> List[str]:
        return self.crud_minio.get_sorted_image_file_names(self.gallery)

    def get_cover(self) -> str:
        bucket_name = self.gallery.bucket_name
        cover_fname = self.crud_minio.get_cover(self.gallery)
        object_name = f"{self.gallery.object_name}{cover_fname}"
        return self.crud_minio.get_url(bucket_name, object_name)

    def get_image(self, image_name: str) -> str:
        bucket_name = self.gallery.bucket_name
        object_name = f"{self.gallery.object_name}{image_name}"
        return self.crud_minio.get_url(bucket_name, object_name)

    def delete(self) -> str:
        self.elastic_client.delete(index=self.index, id=self.gallery.id)
        self.crud_minio.delete_prefix(
            self.gallery.bucket_name, self.gallery.object_name
        )
        return "ok"


# TODO: deprecated
def iter_gallery(minio_client: Minio, bucket_name: str, prefix: str, depth: int):
    try:
        if len(prefix) > 0 and prefix[-1] != "/":
            yield None
        depth -= 1
        objs = minio_client.list_objects(bucket_name, prefix)
        for obj in objs:
            if obj.bucket_name == bucket_name and obj.object_name == prefix:
                continue
            if depth == 0:
                yield obj
            else:
                for obj in iter_gallery(
                    minio_client, bucket_name, obj.object_name, depth
                ):
                    yield obj
    except S3Error:
        # TODO: logging
        pass
    yield None


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


# TODO: deprecated
class CrudSyncGalleryMinioStorage:
    def __init__(
        self,
        minio_storage: MinioStorage,
        elastic_client: Elasticsearch = elastic_client,
        index: str = ELASTICSEARCH_INDEX_GALLERY,
        size: int = ELASTICSEARCH_SIZE,
        batch_size: int = BATCH_SIZE,
        dir_fname: str = DIR_FNAME,
        tag_fname: str = TAG_FNAME,
    ):
        self.minio_storage = minio_storage
        self.minio_path_prefix = f"{Protocol.MINIO.value}-{self.minio_storage.id}://"
        self.minio_client = get_minio_client(
            self.minio_storage.endpoint,
            access_key=self.minio_storage.access_key,
            secret_key=self.minio_storage.secret_key,
        )
        self.crud_minio_gallery = CrudMinioGallery(minio_client=self.minio_client)

        self.elastic_client = elastic_client
        self.index = index

        self.size = size
        self.batch_size = batch_size

        self.dir_fname = dir_fname
        self.tag_fname = tag_fname

        self.cache = set()
        self._elastic_to_minio_batches = []
        self._minio_to_elastic_batches = []

    def sync_gallery(self, bucket_name: str, object_name: str):
        tag_obj_name = f"{object_name}{self.dir_fname}/{self.tag_fname}"
        minio_path = f"{self.minio_path_prefix}{bucket_name}/{object_name}"
        if not self.crud_minio_gallery.exists(bucket_name, tag_obj_name):
            tag = self.crud_minio_gallery.create_tag_in_gallery(
                bucket_name, object_name, minio_path
            )
        else:
            tag = self.crud_minio_gallery.get_tag(bucket_name, tag_obj_name)

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

        if minio_path != tag.path:
            need_to_update = True
            tag.path = minio_path

        if need_to_update:
            self.crud_minio_gallery.put_json(bucket_name, tag_obj_name, tag.dict())

        action = {"_index": self.index, "_id": tag.id, "_source": tag.dict()}
        self._minio_to_elastic_batches.append(action)

        self.cache.add(tag.id)

        if len(self._minio_to_elastic_batches) > self.batch_size:
            helpers.bulk(self.elastic_client, self._minio_to_elastic_batches)
            self._minio_to_elastic_batches = []

    def _sync_minio_to_elastic(self):
        self._minio_to_elastic_batches = []
        for obj in iter_gallery(
            self.minio_client,
            self.minio_storage.bucket_name,
            self.minio_storage.prefix,
            self.minio_storage.depth,
        ):
            if obj is None:
                continue
            self.sync_gallery(obj.bucket_name, obj.object_name)

        if len(self._minio_to_elastic_batches) > 0:
            helpers.bulk(self.elastic_client, self._minio_to_elastic_batches)

    def _sync_elastic_to_minio_batch(self, galleries: Galleries):
        for hit in galleries.hits.hits:
            if not hit.source.path.startswith(self.minio_path_prefix):
                continue
            exists = self.crud_minio_gallery.exists(
                hit.source.bucket_name, hit.source.object_name
            )
            if not exists or hit.id not in self.cache:
                data = {
                    "_index": self.index,
                    "_id": hit.id,
                    "_op_type": "delete",
                }
                self._elastic_to_minio_batches.append(data)
            if len(self._elastic_to_minio_batches) > self.batch_size:
                helpers.bulk(self.elastic_client, self._elastic_to_minio_batches)
                self._elastic_to_minio_batches = []

    def _sync_elastic_to_minio(self):
        count = 0

        dsl = {
            "size": self.size,
            "query": {"match_all": {}},
            "track_total_hits": True,
            "sort": ["_doc"],
        }
        hits = self.elastic_client.search(index=self.index, body=dsl, scroll="1m")
        galleries = Galleries(**hits)

        count += len(galleries.hits.hits)
        self._sync_elastic_to_minio_batch(galleries)

        while galleries.hits.hits:
            hits = self.elastic_client.scroll(
                scroll_id=galleries.scroll_id, scroll="1m"
            )
            galleries = Galleries(**hits)

            count += len(galleries.hits.hits)
            self._sync_elastic_to_minio_batch(galleries)

        if self._elastic_to_minio_batches:
            helpers.bulk(self.elastic_client, self._elastic_to_minio_batches)

    def sync(self):
        import time

        t1 = time.time()
        self._sync_minio_to_elastic()
        t2 = time.time()
        print(t2 - t1)
        self._sync_elastic_to_minio()
        t3 = time.time()
        print(t3 - t2)


async def clean_redundant_elastic(crud: MinioStorage):
    pass
