import io
from pathlib import Path
from typing import Dict, List
from uuid import uuid4

import cv2
from back.crud.elastic import CrudElasticBase, get_source_by_id
from back.crud.minio import CrudMinio, exists, expires, get_minio_client_by_source
from back.db.crud import CrudMinioStorage
from back.db.model import MinioStorage
from back.model.base import Protocol
from back.model.elastic import AnalyzerEnum, QueryBoolean
from back.model.video import Video, VideoOrderedFieldEnum, Videos
from back.session.elastic import elastic_client
from back.session.minio import get_minio_client, minio_client
from back.settings import setting
from back.utils.dt import (
    get_isoformat_with_timezone,
    get_now,
    is_isoformat_with_timezone,
)
from elasticsearch import Elasticsearch, helpers
from fastapi import HTTPException

from minio import Minio

index = setting.elastic_index_video
batch_size = 300
es_size = setting.elastic_size

cache_bucket_name = setting.minio_cache_bucket_name
cover_object_name_prefix = "video/cover"


class CrudElasticVideo(CrudElasticBase[Video]):
    def __init__(
        self,
        elastic_client: Elasticsearch = elastic_client,
        size: int = es_size,
        index: str = index,
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
                {"name.keyword": {"order": "desc"}},
            ],
        )

    @property
    def fields(self):
        if self.analyzer == AnalyzerEnum.DEFAULT.value:
            return [
                "name",
                "other_names",
                "attributes.uploader",
                "attributes.category",
                "attributes.src",
                "labels",
                "tags.*",
            ]
        elif self.analyzer == AnalyzerEnum.NGRAM.value:
            return [
                "name.ngram",
                "other_names.ngram",
                "attributes.uploader",
                "attributes.category",
                "attributes.src.ngram",
                "labels",
                "tags.*",
            ]
        elif self.analyzer == AnalyzerEnum.STANDARD.value:
            return [
                "name.standard",
                "other_names.standard",
                "attributes.uploader",
                "attributes.category",
                "attributes.src.standard",
                "labels",
                "tags.*",
            ]
        return [
            "name",
            "other_names",
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
        other_names: str = None,
        other_names_analyzer: AnalyzerEnum = AnalyzerEnum.DEFAULT,
        other_names_fuzziness: int = 0,
        other_names_bool: QueryBoolean = QueryBoolean.SHOULD,
        category: str = None,
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
            name_field = "name"
            if name_analyzer == AnalyzerEnum.DEFAULT.value:
                name_field = "name"
            elif name_analyzer == AnalyzerEnum.NGRAM.value:
                name_field = "name.ngram"
            elif name_analyzer == AnalyzerEnum.STANDARD.value:
                name_field = "name.standard"
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

        if other_names is not None:
            other_names_field = "other_names"
            if other_names_analyzer == AnalyzerEnum.DEFAULT.value:
                other_names_field = "other_names"
            elif other_names_analyzer == AnalyzerEnum.NGRAM.value:
                other_names_field = "other_names.ngram"
            elif other_names_analyzer == AnalyzerEnum.STANDARD.value:
                other_names_field = "other_names.standard"
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
                                    "analyzer": other_names_analyzer,
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

        return self.query(page, dsl)


class CrudMinioVideo(CrudMinio):
    def __init__(
        self,
        *args,
        cache_minio_client: Minio = minio_client,
        cache_bucket_name: str = cache_bucket_name,
        cover_object_name_prefix: str = cover_object_name_prefix,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.cache_minio_client = cache_minio_client
        self.cache_bucket_name = cache_bucket_name
        self.cover_object_name_prefix = cover_object_name_prefix

    def get_video(self, video: Video) -> str:
        return self.get_url(video.bucket_name, video.object_name)

    def get_cover_bucket_name(self) -> str:
        return self.cache_bucket_name

    def get_cover_object_name(self, video_id: str) -> str:
        return f"{self.cover_object_name_prefix}/{video_id}.png"

    def get_cover(self, video_id: str) -> str:
        return self.get_url(
            self.get_cover_bucket_name(), self.get_cover_object_name(video_id)
        )

    def put_cover(self, video: Video, cover: bytes):
        self.cache_minio_client.put_object(
            self.get_cover_bucket_name(),
            self.get_cover_object_name(video.id),
            io.BytesIO(cover),
            len(cover),
            content_type="image/png",
        )

    def generate_video_cache(self, video: Video, frame: int = 1) -> None:
        if video.id is None:
            return
        if video.attributes.frames is None:
            return

        url = self.get_video(video)
        v = cv2.VideoCapture(url)
        frames = 0
        while True:
            _, current_frame_obj = v.read()

            if current_frame_obj is not None:
                frames += 1
            else:
                break

            if frames == frame:
                cover = cv2.imencode(".png", current_frame_obj)[1].tostring()
                self.put_cover(video, cover)
                break

        if frame > frames:
            # TODO: raise error
            return


def get_video_attrs(
    minio_client: Minio, bucket_name: str, object_name: str, expires=expires
) -> Video:
    url = minio_client.presigned_get_object(bucket_name, object_name, expires=expires)
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


class CrudSyncVideoMinioStorage:
    def __init__(
        self,
        minio_storage: MinioStorage,
        cache_minio_client: Minio = minio_client,
        elastic_client: Elasticsearch = elastic_client,
        index: str = index,
        size: int = es_size,
        batch_size: int = batch_size,
        force: bool = False,
        cache_bucket_name: str = cache_bucket_name,
        cover_object_name_prefix: str = cover_object_name_prefix,
        **kwargs,
    ):
        self.minio_storage = minio_storage
        self.minio_path_prefix = f"{Protocol.MINIO.value}{self.minio_storage.id}://"
        self.minio_client = get_minio_client(
            self.minio_storage.endpoint,
            access_key=self.minio_storage.access_key,
            secret_key=self.minio_storage.secret_key,
        )
        self.crud_minio = CrudMinioVideo(
            minio_client=self.minio_client,
            cache_minio_client=cache_minio_client,
            cache_bucket_name=cache_bucket_name,
            cover_object_name_prefix=cover_object_name_prefix,
            **kwargs,
        )
        self.elastic_client = elastic_client
        self.index = index

        self.size = size
        self.batch_size = batch_size
        self.force = force

        self.available_extensions = [".mp4"]

        self._elastic_to_minio_batches = []
        self._minio_to_elastic_batches = []
        self._video_paths_in_elasitc = {}
        self._video_ids = set()

    @property
    def video_ids(self):
        return self._video_ids

    def _sync_elastic_to_minio_batch(self, videos: Videos):
        for hit in videos.hits.hits:
            if not hit.source.path.startswith(self.minio_path_prefix):
                continue
            self._video_paths_in_elasitc[hit.source.path] = hit.source
            if not exists(
                self.minio_client, hit.source.bucket_name, hit.source.object_name
            ):
                data = {
                    "_index": self.index,
                    "_id": hit.id,
                    "_op_type": "delete",
                }
                self._elastic_to_minio_batches.append(data)
            if len(self._elastic_to_minio_batches) > batch_size:
                helpers.bulk(self.elastic_client, self._elastic_to_minio_batches)
                self._elastic_to_minio_batches = []

    def _sync_elastic_to_minio(self):
        dsl = {
            "size": self.size,
            "query": {"match_all": {}},
            "track_total_hits": True,
            "sort": ["_doc"],
        }
        hits = self.elastic_client.search(index=self.index, body=dsl, scroll="1m")
        videos = Videos(**hits)

        count = 0
        count += len(videos.hits.hits)
        self._sync_elastic_to_minio_batch(videos)

        while videos.hits.hits:
            hits = self.elastic_client.scroll(scroll_id=videos.scroll_id, scroll="1m")
            videos = Videos(**hits)

            count += len(videos.hits.hits)
            self._sync_elastic_to_minio_batch(videos)

        if self._elastic_to_minio_batches:
            helpers.bulk(self.elastic_client, self._elastic_to_minio_batches)

    def _sync_minio_to_elastic(self):
        objects = self.minio_client.list_objects(
            self.minio_storage.bucket_name,
            prefix=self.minio_storage.prefix,
            recursive=True,
        )
        for obj in objects:
            if Path(obj.object_name).suffix not in self.available_extensions:
                continue
            minio_path = f"{self.minio_path_prefix}{obj.bucket_name}/{obj.object_name}"

            video = self._video_paths_in_elasitc.get(minio_path, None)
            if video is not None:
                if not self.force:
                    continue
                else:
                    new_video = get_video_attrs(
                        self.minio_client, obj.bucket_name, obj.object_name
                    )
                    if new_video is None:
                        continue
                    video.attributes.height = new_video.attributes.height
                    video.attributes.width = new_video.attributes.width
                    video.attributes.fps = new_video.attributes.fps
                    video.attributes.duration = new_video.attributes.duration
                    video.attributes.frames = new_video.attributes.frames
            else:
                video = get_video_attrs(
                    self.minio_client, obj.bucket_name, obj.object_name
                )
                if video is None:
                    continue

            video.name = Path(minio_path).name
            video.path = minio_path
            if video.id is None:
                video.id = str(uuid4())
            if video.timestamp is None:
                video.timestamp = get_now()
            if not is_isoformat_with_timezone(video.timestamp):
                video.timestamp = get_isoformat_with_timezone(video.timestamp)

            self._video_ids.add(video.id)
            self.crud_minio.generate_video_cache(video)

            action = {"_index": self.index, "_id": video.id, "_source": video.dict()}
            self._minio_to_elastic_batches.append(action)
            if len(self._minio_to_elastic_batches) > self.batch_size:
                helpers.bulk(self.elastic_client, self._minio_to_elastic_batches)
                self._minio_to_elastic_batches = []

        if len(self._minio_to_elastic_batches) > 0:
            helpers.bulk(self.elastic_client, self._minio_to_elastic_batches)
            self._minio_to_elastic_batches = []

    def sync(self):
        self._sync_elastic_to_minio()
        self._sync_minio_to_elastic()


async def clean():
    pass


def get_video_by_id(
    video_id: str, elastic_client: Elasticsearch = elastic_client, index: str = index
) -> Video:
    return get_source_by_id(video_id, Video, elastic_client=elastic_client, index=index)


class CrudVideo:
    def __init__(
        self,
        video_id: str,
        elastic_client: Elasticsearch = elastic_client,
        crud_minio_storage: CrudMinioStorage = CrudMinioStorage,
        index: str = index,
        cache_minio_client: Minio = minio_client,
        cache_bucket_name: str = cache_bucket_name,
        cover_object_name_prefix: str = cover_object_name_prefix,
    ):
        self.video: Video = get_video_by_id(
            video_id, elastic_client=elastic_client, index=index
        )
        self.crud_minio_storage = crud_minio_storage

        self.elastic_client = elastic_client
        self.index = index

        self.cache_minio_client = cache_minio_client
        self.cache_bucket_name = cache_bucket_name
        self.cover_object_name_prefix = cover_object_name_prefix

    async def init(self):
        minio_client = await get_minio_client_by_source(
            self.video, self.crud_minio_storage
        )
        self.crud_minio = CrudMinioVideo(
            minio_client=minio_client,
            cache_minio_client=self.cache_minio_client,
            cache_bucket_name=self.cache_bucket_name,
            cover_object_name_prefix=self.cover_object_name_prefix,
        )

    def get_video(self) -> str:
        return self.crud_minio.get_video(self.video)

    def set_cover(self, time: float = None, frame: int = None):
        if time is None and frame is None:
            HTTPException(
                status_code=422,
                detail="Time and frame are empty. You must choose one.",
            )
        if time is not None and frame is not None:
            HTTPException(
                status_code=422,
                detail="Time and frame only one are needed.",
            )

        if time is not None:
            frame = time / self.video.attributes.duration * self.video.attributes.frames

        self.crud_minio.generate_video_cache(self.video, frame)

    def get_cover(self) -> str:
        return self.crud_minio.get_cover(self.video.id)

    def update(self, new_video: Video) -> Video:
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

        exists = self.crud_minio.exists(self.video.bucket_name, self.video.object_name)
        if not exists:
            raise HTTPException(
                status_code=404, detail=f"Video id: {self.video.id} not found"
            )

        new_video.timestamp = get_now()
        new_video.labels.sort()
        for key in new_video.tags.keys():
            new_video.tags[key].sort()

        new_video.labels.sort()

        self.elastic_client.index(
            index=self.index, id=new_video.id, body=new_video.dict()
        )

        return new_video


async def get_crud_video(*args, **kwargs) -> CrudVideo:
    crud = CrudVideo(*args, **kwargs)
    await crud.init()
    return crud
