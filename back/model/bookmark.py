from back.db.model import UserBookmarkGallery
from back.model.gallery import Gallery
from pydantic import BaseModel


class GalleryBookmark(BaseModel):
    gallery: Gallery = Gallery()
    bookmark: UserBookmarkGallery = UserBookmarkGallery()
