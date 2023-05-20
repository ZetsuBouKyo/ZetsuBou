from enum import Enum
from typing import Dict, List

from back.model.base import SourceBaseModel
from back.model.elasticsearch import SearchResult
from back.utils.model import DatetimeStr
from pydantic import BaseModel


class VideoOrderedFieldEnum(str, Enum):
    DURATION: str = "attributes.duration"
    NAME: str = "name"
    RATING: str = "attributes.rating"
    TIMESTAMP: str = "timestamp"


class VideoAttributes(BaseModel):
    category: str = None
    rating: int = None

    height: int = None
    width: int = None

    uploader: str = None

    duration: float = None  # in seconds
    fps: int = None
    frames: int = None

    md5: str = None
    src: str = None


class Video(SourceBaseModel):
    id: str = None
    name: str = None
    other_names: List[str] = []
    path: str = None

    attributes: VideoAttributes = VideoAttributes()
    tags: Dict[str, List[str]] = {}
    labels: List[str] = []

    timestamp: DatetimeStr = None


Videos = SearchResult[Video]
