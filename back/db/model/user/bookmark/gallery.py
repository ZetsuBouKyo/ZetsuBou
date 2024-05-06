from typing import Optional

from pydantic import BaseModel, Field
from pydantic.types import NonNegativeInt

from back.model.string import DatetimeStr


class UserBookmarkGalleryCreate(BaseModel):
    user_id: int
    gallery_id: str
    page: NonNegativeInt


class UserBookmarkGalleryUpdate(UserBookmarkGalleryCreate):
    id: int


class UserBookmarkGalleryCreated(UserBookmarkGalleryUpdate):
    modified: DatetimeStr


UserBookmarkGalleryUpdated = UserBookmarkGalleryCreated


class UserBookmarkGallery(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    gallery_id: Optional[str] = None
    page: Optional[NonNegativeInt] = None
    modified: Optional[DatetimeStr] = None
