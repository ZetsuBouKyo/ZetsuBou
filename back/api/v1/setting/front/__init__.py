from fastapi import APIRouter

from .gallery import router as gallery
from .video import router as video

router = APIRouter()

router.include_router(gallery, prefix="/gallery")
router.include_router(video, prefix="/video")
