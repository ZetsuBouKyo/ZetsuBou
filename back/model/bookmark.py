from pydantic import BaseModel

from back.db.model import UserBookmarkGallery
from back.model.gallery import Gallery


class GalleryBookmark(BaseModel):
    gallery: Gallery = Gallery()
    bookmark: UserBookmarkGallery = UserBookmarkGallery()
