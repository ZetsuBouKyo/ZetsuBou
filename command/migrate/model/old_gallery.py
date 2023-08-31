from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field

from back.model.base import SourceBaseModel
from back.model.elasticsearch import SearchResult
from back.utils.dt import datetime_format, datetime_format_db, datetime_format_no_f
from back.utils.model import DatetimeStr


class GalleryOrderedFieldEnum(str, Enum):
    NAME: str = "attributes.name"
    RAW_NAME: str = "attributes.raw_name"
    RATING: str = "attributes.rating"
    TIMESTAMP: str = "timestamp"


class Attributes(BaseModel):
    name: str = Field(default=None, title="Gallery name", example="name")
    raw_name: str = Field(default=None, title="Gallery raw name", example="raw name")
    uploader: str = Field(default=None, title="Gallery uploader", example="uploader")
    category: str = Field(
        default=None,
        title="Gallery category",
        description="We use tag token as category.",
        example="uploader",
    )
    rating: int = Field(
        default=None,
        title="Gallery rating",
        description="Value between 1 and 5.",
        example=5,
    )
    pages: int = Field(
        default=None,
        title="Gallery page",
        description="Number of images in the gallery.",
        example=1,
    )
    src: str = Field(
        default=None,
        title="Gallery source",
        description="Url.",
        example="https://github.com/ZetsuBouKyo/ZetsuBou",
    )


class Gallery(SourceBaseModel):
    id: str = Field(
        default=None,
        title="Gallery ID",
        description="We use uuid4 as the ID by default.",
        example="e172742e-8eaf-4a2f-9c95-9955933f4703",
    )
    path: str = Field(
        default=None,
        title="Gallery path",
        description="File path with custom protocol.",
        example="minio-1://bucket/prefix_1/prefix_1_1",
    )
    group: str = None
    timestamp: DatetimeStr = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",  # noqa
        example="2023-06-07T18:57:12.011241+08:00",
    )
    mtime: DatetimeStr = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",  # noqa
        example="2023-06-07T18:57:12.011241+08:00",
    )

    attributes: Attributes = Field(
        default=Attributes(),
        title="Gallery attributes",
        example={
            "name": "name",
            "raw name": "raw name",
            "uploader": "uploader",
            "category": "category",
            "rating": 5,
            "src": "https://github.com/ZetsuBouKyo/ZetsuBou",
        },
    )
    tags: Dict[str, List[str]] = Field(
        default={},
        title="Tags",
        description="One layer label. We use tokens as labels.",
        example={"Color": ["Red", "Green", "Blue"]},
    )
    labels: List[str] = Field(
        default=[],
        title="Labels",
        description="List of tag tokens.",
        example=["Red", "Green", "Blue"],
    )


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
