from fastapi import APIRouter

from .count import router as count
from .search import router as search

router = APIRouter()
router.include_router(count)
router.include_router(search)
