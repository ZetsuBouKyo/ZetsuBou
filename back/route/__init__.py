from fastapi import APIRouter

from .docs import router as _docs
from .statics import router as _statics
from .views import router as _views

router = APIRouter()

router.include_router(_docs, tags=["Docs"])
router.include_router(_statics, tags=["Statics"])
router.include_router(_views, tags=["Views"])
