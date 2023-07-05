from enum import Enum

from pydantic import BaseModel, Field


class StorageCategoryEnum(int, Enum):
    gallery: int = 0
    video: int = 1


class StorageStat(BaseModel):
    size: int = Field(default=0, description="Size in bytes.")
    num_files: int = Field(default=0, description="Total number of files.")
    num_images: int = Field(
        default=0,
        description="Number of images in gallery. Includes only the images with the given depth.",
    )
    num_mp4s: int = Field(default=0, description="Number of MP4s.")
    num_galleries: int = Field(default=0, description="Number of galleries.")
