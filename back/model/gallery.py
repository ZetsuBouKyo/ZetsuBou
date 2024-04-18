from enum import Enum
from typing import Optional

from pydantic import Field

from back.model.base import SourceBaseModel
from back.model.elasticsearch import SearchResult
from back.model.source import Source, SourceAttributes
from back.settings import setting

DIR_FNAME = setting.gallery_dir_fname
TAG_FNAME = setting.gallery_tag_fname


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
        examples=[1],
    )


class Gallery(Source):
    attributes: Attributes = Field(
        default=Attributes(),
        title="Gallery attributes",
        examples=[
            {
                "category": "category",
                "rating": 5,
                "uploader": "ZetsuBouKyo",
                "pages": 1,
            }
        ],
    )

    _tag_dir: str = DIR_FNAME
    _tag_fname: str = TAG_FNAME

    @property
    def tag_source(cls) -> SourceBaseModel:
        return cls.get_joined_source(cls._tag_dir, cls._tag_fname)


Galleries = SearchResult[Gallery]
