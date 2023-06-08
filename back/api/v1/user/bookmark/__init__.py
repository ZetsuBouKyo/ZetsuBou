from fastapi import APIRouter

from .gallery import router as gallery

router = APIRouter(tags=["Bookmark"])
router.include_router(gallery)
