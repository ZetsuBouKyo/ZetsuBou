from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from back.model.elasticsearch import SearchResult
from back.model.source import Source, SourceAttributes


class GalleryOrderedFieldEnum(str, Enum):
    NAME: str = "name"
    RAW_NAME: str = "raw_name"
    RATING: str = "attributes.rating"
    LAST_UPDATED: str = "last_updated"


class Attributes(SourceAttributes):
    pages: Optional[int] = Field(
        default=None,
        title="Gallery page",
        description="Number of images in the gallery.",
        example=1,
    )


class Gallery(Source):
    attributes: Attributes = Field(
        default=Attributes(),
        title="Gallery attributes",
        example={
            "category": "category",
            "rating": 5,
            "uploader": "ZetsuBouKyo",
            "pages": 1,
        },
    )


Galleries = SearchResult[Gallery]
