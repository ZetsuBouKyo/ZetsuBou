from fastapi import APIRouter

from .image import router as image
from .operation import router as operation
from .query import router as query
from .tag import router as tag

router = APIRouter()
router.include_router(query, tags=["Gallery Query"])
router.include_router(operation, tags=["Gallery Operation"])
router.include_router(tag, tags=["Gallery Tag"])
router.include_router(image, tags=["Gallery Image"])
