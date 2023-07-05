from enum import Enum
from typing import Dict

from PIL.Image import registered_extensions
from pydantic import BaseModel

from back.utils.model import DatetimeStr

ImageFormatEnum = Enum(
    "ImageFormatEnum", {val: key for key, val in registered_extensions().items()}
)


class Image(BaseModel):
    id: str
    gallery_id: str
    width: int
    height: int
    slope: float
    fname: str
    md5: str
    mtime: DatetimeStr


class Images(BaseModel):
    data: Dict[str, Image] = {}
