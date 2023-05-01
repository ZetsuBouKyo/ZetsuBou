from typing import Dict

from back.utils.model import DatetimeStr
from pydantic import BaseModel


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
