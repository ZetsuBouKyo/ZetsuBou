from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from back.model.base import SourceBaseModel
from back.model.string import DatetimeStr
from back.utils.dt import datetime_format, datetime_format_db, datetime_format_no_f


class SourceAttributes(BaseModel):
    category: Optional[str] = Field(
        default=None,
        title="Category",
        description="We use tag token as category.",
        examples=["ZetsuBoyKyo"],
    )
    rating: Optional[int] = Field(
        default=None,
        title="Rating",
        description="Value between 1 and 5.",
        examples=[5],
    )
    uploader: Optional[str] = Field(
        default=None, title="Uploader", examples=["ZetsuBoyKyo"]
    )


class Source(SourceBaseModel):
    id: Optional[str] = Field(
        default=None,
        title="Elasticsearch ID",
        description="We use uuid4 as the ID by default.",
        examples=["e172742e-8eaf-4a2f-9c95-9955933f4703"],
    )

    name: Optional[str] = Field(default=None, title="Name", examples=["name"])
    raw_name: Optional[str] = Field(
        default=None, title="Raw name", examples=["raw name"]
    )
    other_names: List[str] = Field(
        default=[], title="Other names", examples=[["name 1", "name 2"]]
    )
    src: List[Optional[str]] = Field(
        default=[],
        title="Sources",
        description="URLs.",
        examples=[["https://github.com/ZetsuBouKyo/ZetsuBou"]],
    )

    last_updated: Optional[DatetimeStr] = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",
        examples=["2023-06-07T18:57:12.011241+08:00"],
    )
    publication_date: Optional[DatetimeStr] = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",
        examples=["2023-06-07T18:57:12.011241+08:00"],
    )
    upload_date: Optional[DatetimeStr] = Field(
        default=None,
        description=f"We use ISO format with timezone. Our datetime formats are `{datetime_format_db}`, `{datetime_format}`, and `{datetime_format_no_f}`.",
        examples=["2023-06-07T18:57:12.011241+08:00"],
    )

    labels: List[str] = Field(
        default=[],
        title="Labels",
        description="List of tag tokens.",
        examples=[["Red", "Green", "Blue"]],
    )
    tags: Dict[str, List[str]] = Field(
        default={},
        title="Tags",
        description="One layer label. We use tokens as labels.",
        examples=[{"Color": ["Red", "Green", "Blue"]}],
    )
