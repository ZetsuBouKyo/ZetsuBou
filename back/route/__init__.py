from fastapi import APIRouter

from .docs import router as docs
from .statics import router as statics
from .views import router as views

router = APIRouter()

router.include_router(docs, tags=["Docs"])
router.include_router(statics, tags=["Statics"])
router.include_router(views, tags=["Views"])
