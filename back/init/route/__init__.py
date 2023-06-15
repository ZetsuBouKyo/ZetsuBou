from back.route.docs import router as docs
from back.route.statics import router as statics
from fastapi import APIRouter

from .api import router as api
from .views import router as views

router = APIRouter()

router.include_router(api)
router.include_router(docs, tags=["Docs"])
router.include_router(statics, tags=["Statics"])
router.include_router(views, tags=["Views"])
