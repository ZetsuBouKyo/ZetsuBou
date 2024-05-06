from fastapi import APIRouter

from .elastic_count import router as _elastic_count
from .quest import router as _quest

router = APIRouter()
router.include_router(_elastic_count)
router.include_router(_quest)
