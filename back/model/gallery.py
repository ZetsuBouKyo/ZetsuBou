from enum import Enum
from typing import Dict, List

from back.model.base import SourceBaseModel
from back.model.elasticsearch import SearchResult
from back.utils.model import DatetimeStr
from pydantic import BaseModel


class GalleryOrderedFieldEnum(str, Enum):
    NAME: str = "attributes.name"
    RAW_NAME: str = "attributes.raw_name"
    RATING: str = "attributes.rating"
    TIMESTAMP: str = "timestamp"


class Attributes(BaseModel):
    name: str = None
    raw_name: str = None
    uploader: str = None
    category: str = None
    rating: int = None
    src: str = None


class Gallery(SourceBaseModel):
    id: str = None
    path: str = None
    group: str = None
    timestamp: DatetimeStr = None
    mtime: DatetimeStr = None

    attributes: Attributes = Attributes()
    tags: Dict[str, List[str]] = {}
    labels: List[str] = []


Galleries = SearchResult[Gallery]


class Page(BaseModel):
    total: int = 0
    current: int = 0


class Preview(BaseModel):
    category: str = None
    title: str = None
    imgUrl: str = None
    linkUrl: str = None


class PreviewList(BaseModel):
    page: Page = Page()
    items: List[Preview] = []
