from pydantic import BaseModel, Field

from back.utils.model import DatetimeStr


class UserBookmarkGalleryCreate(BaseModel):
    user_id: int
    gallery_id: str
    page: int = Field(default=..., description="0-based image index.")


class UserBookmarkGalleryUpdate(UserBookmarkGalleryCreate):
    id: int


class UserBookmarkGalleryCreated(UserBookmarkGalleryUpdate):
    id: int
    modified: DatetimeStr


UserBookmarkGalleryUpdated = UserBookmarkGalleryCreated


class UserBookmarkGallery(BaseModel):
    id: int = None
    user_id: int = None
    gallery_id: str = None
    page: int = Field(default=None, description="0-based image index.")
    modified: DatetimeStr = None
