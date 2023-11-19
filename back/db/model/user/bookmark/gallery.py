from typing import Optional

from pydantic import BaseModel, Field

from back.utils.model import DatetimeStr


class UserBookmarkGalleryCreate(BaseModel):
    user_id: int
    gallery_id: str
    page: Optional[int] = Field(default=..., description="0-based image index.")


class UserBookmarkGalleryUpdate(UserBookmarkGalleryCreate):
    id: int


class UserBookmarkGalleryCreated(UserBookmarkGalleryUpdate):
    modified: DatetimeStr


UserBookmarkGalleryUpdated = UserBookmarkGalleryCreated


class UserBookmarkGallery(BaseModel):
    id: Optional[int] = None
    user_id: Optional[int] = None
    gallery_id: Optional[str] = None
    page: Optional[int] = Field(default=None, description="0-based image index.")
    modified: Optional[DatetimeStr] = None
