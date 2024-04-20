from fastapi import APIRouter

from back.api.v1.gallery.image import router as image
from back.api.v1.gallery.operation import router as operation
from back.api.v1.gallery.query import router as query
from back.api.v1.gallery.tag import router as tag

router = APIRouter(prefix="/gallery", tags=["Gallery"])
router.include_router(query)
router.include_router(operation)
router.include_router(tag)
router.include_router(image)
