from fastapi import APIRouter

from .count import router as _count
from .search import router as _search

router = APIRouter()
router.include_router(_count)
router.include_router(_search)
