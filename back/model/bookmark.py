from typing import Dict

from pydantic import BaseModel, Field


class Bookmark(BaseModel):
    user_id: int = None
    gallery: Dict[str, int] = Field(
        default={},
        title="Gallery bookmark",
        description="Bookmark for galleries. The key is the gallery ID and the value is the page number.",  # noqa
        example={
            "a6473dcd-0823-4a0e-a20e-2f5fd8fed152": 1,
            "e172742e-8eaf-4a2f-9c95-9955933f4703": 100,
        },
    )
    video: Dict[str, int] = Field(
        default={},
        title="Video bookmark",
        description="Bookmark for videos. The key is the video ID and the value is the time in seconds.",  # noqa
        example={
            "8592d507-bc32-493a-9fd1-8a4952b33c4f": 1,
            "0f84c214-5b37-4f77-b49f-171517ab8584": 314,
        },
    )
