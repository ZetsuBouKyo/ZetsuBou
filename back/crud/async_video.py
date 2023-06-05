import io
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

import cv2
from back.crud.async_elasticsearch import CrudAsyncElasticsearchBase
from back.crud.async_progress import Progress
from back.logging import logger_webapp
from back.model.base import SourceBaseModel, SourceProtocolEnum
from back.model.elasticsearch import AnalyzerEnum, QueryBoolean
from back.model.task import ZetsuBouTaskProgressEnum
from back.model.video import Video, VideoOrderedFieldEnum, Videos
from back.session.async_elasticsearch import async_elasticsearch
from back.session.storage import get_app_storage_session, get_storage_session_by_source
from back.session.storage.async_s3 import AsyncS3Session
from back.settings import setting
from back.utils.dt import (
    get_isoformat_with_timezone,
    get_now,
    is_isoformat_with_timezone,
)
from fastapi import HTTPException

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk, async_scan

ELASTICSEARCH_INDEX_VIDEO = setting.elastic_index_video
ELASTICSEARCH_SIZE = setting.elastic_size

BATCH_SIZE = 300

STORAGE_PROTOCOL = setting.storage_protocol
STORAGE_CACHE = setting.storage_cache
VIDEO_COVER_HOME = "video/cover"

elasticsearch_video_analyzer = {
    AnalyzerEnum.DEFAULT.value: [
        "path.url",
        "name.default",
        "other_names.default",
        "attributes.uploader",
        "attributes.category",
        "attributes.src.url",
        "labels",
        "tags.*",
    ],
    AnalyzerEnum.KEYWORD.value: [
        "path.keyword",
        "attributes.name.keyword",
        "attributes.raw_name.keyword",
        "attributes.uploader",
        "attributes.category",
        "attributes.src.keyword",
        "labels",
        "tags.*",
    ],
    AnalyzerEnum.NGRAM.value: [
        "path.ngram",
        "name.ngram",
        "other_names.ngram",
        "attributes.uploader",
        "attributes.category",
        "attributes.src.ngram",
        "labels",
        "tags.*",
    ],
    AnalyzerEnum.STANDARD.value: [
        "path.standard",
        "name.standard",
        "other_names.standard",
        "attributes.uploader",
        "attributes.category",
        "attributes.src.standard",
        "labels",
        "tags.*",
    ],
    AnalyzerEnum.URL.value: ["path.url", "attributes.src.url"],
}


def get_sync_video_progress_id(protocol: SourceProtocolEnum, id: int):
    return f"{ZetsuBouTaskProgressEnum.SYNC_STORAGE}.{protocol}.{id}"


class CrudAsyncElasticsearchVideo(CrudAsyncElasticsearchBase[Video]):
    def __init__(
        self,
        hosts: List[str] = None,
        size: int = 10,
        index: str = ELASTICSEARCH_INDEX_VIDEO,
        analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        sorting: List[Any] = [
            "_score",
            {"timestamp": {"order": "desc", "unmapped_type": "long"}},
            {"mtime": {"order": "desc", "unmapped_type": "long"}},
            {"name.keyword": {"order": "desc"}},
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
        return elasticsearch_video_analyzer.get(self.analyzer, None)

    async def get_by_id(self, id: str) -> Video:
        return Video(**await self.get_source_by_id(id))

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
        other_names: str = None,
        other_names_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        other_names_fuzziness: int = 0,
        other_names_bool: QueryBoolean = QueryBoolean.SHOULD,
        src: str = None,
        src_analyzer: AnalyzerEnum = AnalyzerEnum.URL,
        src_fuzziness: int = 0,
        src_bool: QueryBoolean = QueryBoolean.SHOULD,
        path: str = None,
        path_analyzer: AnalyzerEnum = AnalyzerEnum.URL,
        path_fuzziness: int = 0,
        path_bool: QueryBoolean = QueryBoolean.SHOULD,
        category: str = None,
        uploader: str = None,
        rating_gte: int = None,
        rating_lte: int = None,
        height_gte: int = None,
        height_lte: int = None,
        width_gte: int = None,
        width_lte: int = None,
        duration_gte: float = None,
        duration_lte: float = None,
        order_by: VideoOrderedFieldEnum = None,
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
            sorting.append({"name.keyword": {"order": "desc"}})
        elif is_desc:
            sorting.append({order_by: {"order": "desc"}})
        else:
            sorting.append({order_by: {"order": "asc"}})

        dsl["sort"] = sorting

        if keywords is not None:
            keywords = keywords.split()
            self.analyzer = keywords_analyzer
            for keyword in keywords:
                dsl["query"]["bool"][keywords_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": keyword,
                                    "fuzziness": keywords_fuzziness,
                                    "fields": self.fields,
                                }
                            }
                        }
                    }
                )
        if name is not None:
            name_field = f"name.{name_analyzer}"
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
                                }
                            }
                        }
                    }
                )

        if other_names is not None:
            other_names_field = f"other_names.{other_names_analyzer}"
            other_names = other_names.split()
            for n in other_names:
                dsl["query"]["bool"][other_names_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": n,
                                    "fuzziness": other_names_fuzziness,
                                    "fields": [other_names_field],
                                }
                            }
                        }
                    }
                )

        if src is not None:
            src_field = f"attributes.src.{src_analyzer}"
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
                                }
                            }
                        }
                    }
                )

        if path is not None:
            path_field = f"path.{path_analyzer}"
            path = path.split()
            for n in path:
                dsl["query"]["bool"][path_bool].append(
                    {
                        "constant_score": {
                            "filter": {
                                "multi_match": {
                                    "query": n,
                                    "fuzziness": path_fuzziness,
                                    "fields": [path_field],
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

        if height_gte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.height": {"gte": height_gte}}}
            )
        if height_lte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.height": {"lte": height_lte}}}
            )

        if width_gte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.width": {"gte": width_gte}}}
            )
        if width_lte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.width": {"lte": width_lte}}}
            )

        if duration_gte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.duration": {"gte": duration_gte}}}
            )
        if duration_lte is not None:
            dsl["query"]["bool"]["must"].append(
                {"range": {"attributes.duration": {"lte": duration_lte}}}
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

    async def match_phrase_prefix(self, keywords: str, size: int = 5) -> Videos:
        query = {
            "bool": {
                "should": [
                    {
                        "match_phrase_prefix": {
                            "attributes.name.ngram": {"query": keywords}
                        }
                    },
                    {
                        "match_phrase_prefix": {
                            "attributes.raw_name.ngram": {"query": keywords}
                        }
                    },
                ]
            }
        }
        _resp = await self.async_elasticsearch.search(
            index=self.index, query=query, size=size
        )
        sources = Videos(**_resp)
        return sources


async def get_video_by_video_id(id: str) -> Video:
    crud = CrudAsyncElasticsearchVideo(is_from_setting_if_none=True)
    return await crud.get_by_id(id)


def _get_cover_source(
    protocol: SourceProtocolEnum, cache_home: str, cover_home: str, video_id: str
) -> SourceBaseModel:
    return SourceBaseModel(
        path=f"{protocol}://{cache_home}/{cover_home}/{video_id}.png"
    )


async def _put_cover(
    storage_session: AsyncS3Session, cover_source: SourceBaseModel, cover: bytes
):
    await storage_session.put_object(
        cover_source,
        io.BytesIO(cover),
        content_type="image/png",
    )


async def _generate_cover(
    app_storage_protocol: SourceProtocolEnum,
    app_storage_session: AsyncS3Session,
    storage_session: AsyncS3Session,
    video: Video,
    cache_home: str,
    cover_home: str,
    frame: int = 0,
):
    if video.id is None:
        return
    if video.attributes.frames is None:
        return

    cover_source = _get_cover_source(
        app_storage_protocol, cache_home, cover_home, video.id
    )

    url = await storage_session.get_url(video)
    v = cv2.VideoCapture(url)

    frames = 0
    while frames < video.attributes.frames:
        v.grab()
        if frames == frame:
            _, current_frame_obj = v.retrieve()
            cover = cv2.imencode(".png", current_frame_obj)[1].tostring()
            await _put_cover(app_storage_session, cover_source, cover)
            return
        frames += 1

    _, current_frame_obj = v.retrieve()
    cover = cv2.imencode(".png", current_frame_obj)[1].tostring()
    await _put_cover(app_storage_session, cover_source, cover)


class CrudAsyncVideo:
    def __init__(
        self,
        video_id: str,
        video: Video = None,
        hosts: List[str] = None,
        index: str = None,
        cache_home: str = None,
        cover_home: str = None,
        app_storage_protocol: SourceProtocolEnum = None,
        app_storage_session: AsyncS3Session = None,
        storage_session: AsyncS3Session = None,
        is_from_setting_if_none: bool = False,
    ):
        self.video_id = video_id
        self.video = video

        self.hosts = hosts
        self.async_elasticsearch = AsyncElasticsearch(self.hosts)
        self.index = index
        self.cache_home = cache_home
        self.cover_home = cover_home
        self.app_storage_protocol = app_storage_protocol
        self.app_storage_session = app_storage_session
        self.storage_session = storage_session

        self.is_from_setting_if_none = is_from_setting_if_none
        if self.is_from_setting_if_none:
            if self.hosts is None:
                self.async_elasticsearch = async_elasticsearch
            if self.index is None:
                self.index = ELASTICSEARCH_INDEX_VIDEO
            if self.cache_home is None:
                self.cache_home = STORAGE_CACHE
            if self.cover_home is None:
                self.cover_home = VIDEO_COVER_HOME
            if self.app_storage_protocol is None:
                self.app_storage_protocol = STORAGE_PROTOCOL

    async def init(self):
        if self.video is None:
            self.video = await get_video_by_video_id(self.video_id)
        if self.is_from_setting_if_none:
            if self.app_storage_session is None:
                self.app_storage_session = get_app_storage_session(
                    is_from_setting_if_none=True
                )
            if self.storage_session is None:
                self.storage_session = await get_storage_session_by_source(self.video)

    async def get_video(self) -> str:
        async with self.storage_session:
            return await self.storage_session.get_url(self.video)

    @property
    def cover_source(self) -> SourceBaseModel:
        if not hasattr(self, "_cover_source"):
            self._cover_source = _get_cover_source(
                self.app_storage_protocol,
                self.cache_home,
                self.cover_home,
                self.video_id,
            )
        return self._cover_source

    async def get_cover(self) -> str:
        async with self.storage_session:
            return await self.storage_session.get_url(self.cover_source)

    async def put_cover(self, cover: bytes):
        async with self.app_storage_session:
            await _put_cover(self.app_storage_session, self.cover_source, cover)

    async def generate_cover(self, frame: int = 0):
        async with self.app_storage_session, self.storage_session:
            await _generate_cover(
                self.app_storage_protocol,
                self.app_storage_session,
                self.storage_session,
                self.video,
                self.cache_home,
                self.cover_home,
                frame=frame,
            )

    async def update(self, new_video: Video) -> Video:
        if new_video.id != self.video.id:
            raise HTTPException(
                status_code=409,
                detail="Conflict between elastic video and new video ids",
            )
        if new_video.path != self.video.path:
            raise HTTPException(
                status_code=409,
                detail="Conflict between elastic video and new video paths",
            )

        async with self.storage_session:
            exists = await self.storage_session.exists(self.video)
        if not exists:
            raise HTTPException(
                status_code=404, detail=f"Video id: {self.video.id} not found"
            )

        new_video.timestamp = get_now()
        new_video.labels.sort()
        for key in new_video.tags.keys():
            new_video.tags[key].sort()

        new_video.labels.sort()

        await self.async_elasticsearch.index(
            index=self.index, id=new_video.id, body=new_video.dict()
        )

        return new_video


async def get_crud_async_video(video_id: str) -> CrudAsyncVideo:
    crud = CrudAsyncVideo(video_id, is_from_setting_if_none=True)
    await crud.init()
    return crud


async def _get_video_attrs(storage_session: AsyncS3Session, video: Video) -> Video:
    url = await storage_session.get_url(video)
    v = cv2.VideoCapture(url)

    width, height = None, None
    has_frame = 0
    while True:
        _, frame = v.read()

        if frame is not None:
            has_frame += 1
            width = frame.shape[1]
            height = frame.shape[0]
        break

    if not has_frame:
        return None

    fps = v.get(cv2.CAP_PROP_FPS)
    duration = None
    frame_count = int(v.get(cv2.CAP_PROP_FRAME_COUNT))
    if type(frame_count) is int and fps > 0:
        duration = frame_count / fps

    return Video(
        **{
            "attributes": {
                "height": height,
                "width": width,
                "duration": duration,
                "fps": fps,
                "frames": frame_count,
            }
        }
    )


class CrudAsyncVideoSync:
    def __init__(
        self,
        storage_session: AsyncS3Session,
        storage_protocol: SourceProtocolEnum,
        storage_id: int,
        root_source: SourceBaseModel,
        depth: int,
        hosts: List[str] = None,
        index: str = None,
        size: int = None,
        batch_size: int = None,
        force: bool = False,
        cache_home: str = None,
        cover_home: str = None,
        app_storage_protocol: SourceProtocolEnum = None,
        app_storage_session: AsyncS3Session = None,
        progress_id: str = None,
        progress_initial: float = 0,
        progress_final: float = 100.0,
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
        self.size = size
        self.batch_size = batch_size
        self.force = force

        self.cache_home = cache_home
        self.cover_home = cover_home
        self.app_storage_protocol = app_storage_protocol
        self.app_storage_session = app_storage_session

        self.async_elasticsearch = AsyncElasticsearch(self.hosts)

        self.progress_initial = progress_initial
        self.progress_final = progress_final
        self.progress_interval = self.progress_final - self.progress_initial
        self.progress_id = progress_id
        if self.progress_id is None:
            self.progress_id = get_sync_video_progress_id(
                self.storage_protocol, self.storage_id
            )
        self.is_progress = is_progress

        if is_from_setting_if_none:
            if self.hosts is None:
                self.async_elasticsearch = async_elasticsearch
            if self.index is None:
                self.index = ELASTICSEARCH_INDEX_VIDEO
            if self.size is None:
                self.size = ELASTICSEARCH_SIZE
            if self.batch_size is None:
                self.batch_size = BATCH_SIZE
            if self.cache_home is None:
                self.cache_home = STORAGE_CACHE
            if self.cover_home is None:
                self.cover_home = VIDEO_COVER_HOME
            if self.app_storage_protocol is None:
                self.app_storage_protocol = STORAGE_PROTOCOL

        self.available_extensions = [".mp4"]

        self._elasticsearch_to_storage_batches = []
        self._storage_to_elasticsearch_batches = []
        self._video_paths_in_elasitcsearch = {}

    async def init(self):
        if self.is_from_setting_if_none and self.app_storage_session is None:
            self.app_storage_session = get_app_storage_session(
                is_from_setting_if_none=True
            )

    async def send_bulk(self, batches: List[dict]):
        await async_bulk(self.async_elasticsearch, batches)
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
                            "fields": [f"path.{AnalyzerEnum.URL}"],
                        }
                    }
                }
            },
            "track_total_hits": True,
        }

    async def _sync_video_elasticsearch_to_storage(self, doc: dict):
        source = doc.get("_source", None)
        if source is None:
            return

        video = Video(**source)

        if video._scheme != self.root_source._scheme:
            return

        exists = await self.storage_session.exists(video)
        if not exists:
            self._elasticsearch_to_storage_batches.append(
                {
                    "_index": self.index,
                    "_id": video.id,
                    "_op_type": "delete",
                }
            )
        else:
            self._video_paths_in_elasitcsearch[video.path] = video

        if len(self._elasticsearch_to_storage_batches) > self.batch_size:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def _sync_video_storage_to_elasticsearch(self, source: SourceBaseModel):
        if Path(source.path).suffix not in self.available_extensions:
            return

        video = self._video_paths_in_elasitcsearch.get(source.path, None)
        if video is not None:
            if not self.force:
                return
            else:
                new_video = await _get_video_attrs(self.storage_session, video)
                if new_video is None:
                    return
                video.attributes.height = new_video.attributes.height
                video.attributes.width = new_video.attributes.width
                video.attributes.fps = new_video.attributes.fps
                video.attributes.duration = new_video.attributes.duration
                video.attributes.frames = new_video.attributes.frames
        else:
            video = await _get_video_attrs(self.storage_session, source)
            if video is None:
                return

        video.name = Path(source.path).name
        video.path = source.path
        if video.id is None:
            video.id = str(uuid4())
        if video.timestamp is None:
            video.timestamp = get_now()
        if not is_isoformat_with_timezone(video.timestamp):
            video.timestamp = get_isoformat_with_timezone(video.timestamp)

        await _generate_cover(
            self.app_storage_protocol,
            self.app_storage_session,
            self.storage_session,
            video,
            self.cache_home,
            self.cover_home,
        )

        action = {"_index": self.index, "_id": video.id, "_source": video.dict()}
        self._storage_to_elasticsearch_batches.append(action)

        if len(self._storage_to_elasticsearch_batches) > self.batch_size:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

    async def _sync_elasticsearch_to_storage_without_progress(self):
        query = self.dsl

        async for doc in async_scan(
            client=self.async_elasticsearch, query=query, index=self.index
        ):
            await self._sync_video_elasticsearch_to_storage(doc)

        if len(self._elasticsearch_to_storage_batches) > 0:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def _sync_storage_to_elasticsearch_without_progress(self):
        sources = await self.storage_session.list_nested_sources(self.root_source)
        for source in sources:
            await self._sync_video_storage_to_elasticsearch(source)

        if len(self._storage_to_elasticsearch_batches) > 0:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

    async def _count_storage(self):
        self._sources = await self.storage_session.list_nested_sources(self.root_source)

        self._storage_to_elasticsearch_num = len(self._sources)

        logger_webapp.debug(
            f"storage to elasticsearch (number): {self._storage_to_elasticsearch_num}"
        )

    async def _count_elasticsearch(self):
        dsl = self.dsl

        resp = await self.async_elasticsearch.search(index=self.index, body=dsl)
        self._elasticsearch_to_storage_num = resp["hits"]["total"]["value"]

        logger_webapp.debug(
            f"elasticsearch to storage (number): {self._elasticsearch_to_storage_num}"
        )

    async def _sync_elasticsearch_to_storage(self):
        query = self.dsl

        self._elasticsearch_to_storage_final = (
            self._elasticsearch_to_storage_num
            / (self._storage_to_elasticsearch_num + self._elasticsearch_to_storage_num)
            * self.progress_interval
        )

        async for doc in Progress(
            async_scan(client=self.async_elasticsearch, query=query, index=self.index),
            id=self.progress_id,
            initial=self.progress_initial,
            final=self._elasticsearch_to_storage_final,
            total=self._elasticsearch_to_storage_num,
            is_from_setting_if_none=True,
        ):
            await self._sync_video_elasticsearch_to_storage(doc)

        if len(self._elasticsearch_to_storage_batches) > 0:
            await self.send_bulk(self._elasticsearch_to_storage_batches)

    async def _sync_storage_to_elasticsearch(self):
        async for source in Progress(
            self._sources,
            id=self.progress_id,
            initial=self._elasticsearch_to_storage_final,
            final=self.progress_final,
            total=self._elasticsearch_to_storage_num,
            is_from_setting_if_none=True,
        ):
            await self._sync_video_storage_to_elasticsearch(source)

        if len(self._storage_to_elasticsearch_batches) > 0:
            await self.send_bulk(self._storage_to_elasticsearch_batches)

    async def sync(self):
        logger_webapp.debug(f"storage protocol: {self.storage_protocol}")
        logger_webapp.debug(f"storage id: {self.storage_id}")
        logger_webapp.debug(f"elasticsearch index: {self.index}")
        logger_webapp.debug(f"is progress: {self.is_progress}")
        logger_webapp.debug(f"progress id: {self.progress_id}")

        async with self.app_storage_session, self.storage_session:
            if self.is_progress:
                await self._count_storage()
                await self._count_elasticsearch()
                await self._sync_elasticsearch_to_storage()
                await self._sync_storage_to_elasticsearch()

            else:
                await self._sync_elasticsearch_to_storage_without_progress()
                await self._sync_storage_to_elasticsearch_without_progress()
