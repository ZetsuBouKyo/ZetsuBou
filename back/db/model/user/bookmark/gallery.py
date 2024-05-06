from pydantic import BaseModel
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


UserBookmarkGallery = UserBookmarkGalleryUpdated = UserBookmarkGalleryCreated
