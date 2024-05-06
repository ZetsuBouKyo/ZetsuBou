from fastapi import APIRouter

from back.api.v1.gallery.image import router as _image
from back.api.v1.gallery.operation import router as _operation
from back.api.v1.gallery.query import router as _query
from back.api.v1.gallery.tag import router as _tag

router = APIRouter(prefix="/gallery", tags=["Gallery"])
router.include_router(_query)
router.include_router(_operation)
router.include_router(_tag)
router.include_router(_image)
