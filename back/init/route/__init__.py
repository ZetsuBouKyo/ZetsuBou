from fastapi import APIRouter

from back.api.v1.init import router as _init
from back.api.v1.setting import router as _setting
from back.route.docs import router as _docs
from back.route.statics import router as _statics

from .views import router as _views

router = APIRouter()

router.include_router(_init, prefix="/api/v1")
router.include_router(_setting, prefix="/api/v1")
router.include_router(_docs, tags=["Docs"])
router.include_router(_statics, tags=["Statics"])
router.include_router(_views, tags=["Views"])
