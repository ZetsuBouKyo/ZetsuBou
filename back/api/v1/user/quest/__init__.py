from fastapi import APIRouter

from .category import router as category
from .elastic_count import router as elastic_count
from .quest import router as quest

router = APIRouter()
router.include_router(elastic_count, tags=["User Elastic Count Quest"])
router.include_router(category, tags=["User Quest Category"])
router.include_router(quest, tags=["User Quest"])
