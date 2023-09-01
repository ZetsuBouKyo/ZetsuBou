from enum import Enum
from typing import Optional

from back.model.elasticsearch import SearchResult
from back.model.source import Source, SourceAttributes


class VideoOrderedFieldEnum(str, Enum):
    DURATION: str = "attributes.duration"
    NAME: str = "name"
    RATING: str = "attributes.rating"
    LAST_UPDATED: str = "last_updated"


class VideoAttributes(SourceAttributes):
    width: Optional[int] = None
    height: Optional[int] = None

    duration: Optional[float] = None  # in seconds
    fps: Optional[int] = None
    frames: Optional[int] = None

    md5: Optional[str] = None


class Video(Source):
    attributes: VideoAttributes = VideoAttributes()


Videos = SearchResult[Video]
