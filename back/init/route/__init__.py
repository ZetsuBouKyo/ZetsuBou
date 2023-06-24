from back.api.v1.init import router as init
from back.api.v1.setting import router as setting
from back.route.docs import router as docs
from back.route.statics import router as statics
from fastapi import APIRouter

from .views import router as views

router = APIRouter()

router.include_router(init, prefix="/api/v1")
router.include_router(setting, prefix="/api/v1")
router.include_router(docs, tags=["Docs"])
router.include_router(statics, tags=["Statics"])
router.include_router(views, tags=["Views"])
