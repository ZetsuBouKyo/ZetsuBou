from back.utils.model import DatetimeStr
from pydantic import BaseModel, Field


class UserBookmarkGalleryCreate(BaseModel):
    user_id: int
    gallery_id: str
    page: int = Field(default=..., description="0-based image index.")


class UserBookmarkGalleryUpdate(UserBookmarkGalleryCreate):
    id: int


class UserBookmarkGalleryCreated(UserBookmarkGalleryUpdate):
    id: int
    modified: DatetimeStr


UserBookmarkGallery = UserBookmarkGalleryUpdated = UserBookmarkGalleryCreated
