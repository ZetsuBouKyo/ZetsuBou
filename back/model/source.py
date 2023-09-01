from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from back.model.base import SourceBaseModel
from back.utils.dt import datetime_format, datetime_format_db, datetime_format_no_f
from back.utils.model import DatetimeStr


class SourceAttributes(BaseModel):
    category: Optional[str] = Field(
        default=None,
        title="Category",
        description="We use tag token as category.",
        example="ZetsuBoyKyo",
    )
    rating: Optional[int] = Field(
        default=None,
        title="Rating",
        description="Value between 1 and 5.",
        example=5,
    )
    uploader: Optional[str] = Field(default=None, title="Uploader", example="uploader")


class Source(SourceBaseModel):
    id: Optional[str] = Field(
        default=None,
        title="Elasticsearch ID",
        description="We use uuid4 as the ID by default.",
        example="e172742e-8eaf-4a2f-9c95-9955933f4703",
    )

    name: Optional[str] = Field(default=None, title="Name", example="name")
    raw_name: Optional[str] = Field(default=None, title="Raw name", example="raw name")
    other_names: List[str] = Field(
        default=[], title="Other names", example=["name 1", "name 2"]
    )
    src: List[Optional[str]] = Field(
        default=[],
        title="Sources",
        description="URLs.",
        example=["https://github.com/ZetsuBouKyo/ZetsuBou"],
    )

    last_updated: Optional[DatetimeStr] = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",
        example="2023-06-07T18:57:12.011241+08:00",
    )
    publication_date: Optional[DatetimeStr] = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",
        example="2023-06-07T18:57:12.011241+08:00",
    )
    upload_date: Optional[DatetimeStr] = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",
        example="2023-06-07T18:57:12.011241+08:00",
    )

    labels: List[str] = Field(
        default=[],
        title="Labels",
        description="List of tag tokens.",
        example=["Red", "Green", "Blue"],
    )
    tags: Dict[str, List[str]] = Field(
        default={},
        title="Tags",
        description="One layer label. We use tokens as labels.",
        example={"Color": ["Red", "Green", "Blue"]},
    )
