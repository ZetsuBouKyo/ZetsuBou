from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from back.model.source import SourceBaseModel


class StorageCategoryEnum(int, Enum):
    gallery: int = 0
    video: int = 1


class StorageGalleryCodeEnum(int, Enum):
    DOES_NOT_HAVE_IMAGES: int = 0  # The path does not have images.
    FILES_IN_THE_INTERNAL_NODES_OF_THE_STORAGE_PATH: int = (
        1  # There are images in the internal nodes of the storage path.
    )


class StorageGallery(SourceBaseModel):
    code: StorageGalleryCodeEnum


class StorageGalleries(BaseModel):
    percentage: Optional[float] = None
    galleries: List[StorageGallery] = []


class StorageStat(BaseModel):
    size: int = Field(default=0, description="Size in bytes.")
    num_files: int = Field(default=0, description="Total number of files.")
    num_images: int = Field(
        default=0,
        description="Number of images in gallery. Includes only the images with the given depth.",
    )
    num_mp4s: int = Field(default=0, description="Number of MP4s.")
    num_galleries: int = Field(default=0, description="Number of galleries.")
