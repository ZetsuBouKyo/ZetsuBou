from fastapi import APIRouter

from .gallery import router as _gallery

router = APIRouter(tags=["Bookmark"])
router.include_router(_gallery)
