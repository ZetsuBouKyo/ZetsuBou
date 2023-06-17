from fastapi import APIRouter

from .elastic_count import router as elastic_count
from .quest import router as quest

router = APIRouter()
router.include_router(elastic_count)
router.include_router(quest)
