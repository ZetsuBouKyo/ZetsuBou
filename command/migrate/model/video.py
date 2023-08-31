from enum import Enum

from back.model.elasticsearch import SearchResult
from back.model.source import Source, SourceAttributes


class VideoOrderedFieldEnum(str, Enum):
    DURATION: str = "attributes.duration"
    NAME: str = "name"
    RATING: str = "attributes.rating"
    TIMESTAMP: str = "timestamp"


class VideoAttributes(SourceAttributes):
    width: int = None
    height: int = None

    duration: float = None  # in seconds
    fps: int = None
    frames: int = None

    md5: str = None


class Video(Source):
    attributes: VideoAttributes = VideoAttributes()


Videos = SearchResult[Video]
