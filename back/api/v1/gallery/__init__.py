from fastapi import APIRouter

from .image import router as image
from .operation import router as operation
from .query import router as query
from .tag import router as tag

router = APIRouter(prefix="/gallery", tags=["Gallery"])
router.include_router(query)
router.include_router(operation)
router.include_router(tag)
router.include_router(image)
