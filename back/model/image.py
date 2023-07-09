from enum import Enum
from typing import Dict

from PIL.Image import registered_extensions
from pydantic import BaseModel

from back.utils.model import DatetimeStr

_image_formats = {}
for extension in registered_extensions().keys():
    key = extension.replace(".", "").upper()
    _image_formats[key] = extension

ImageFormatEnum = Enum("ImageFormatEnum", _image_formats)


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
