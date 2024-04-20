from fastapi import APIRouter

from back.api.v1.setting.front import router as front
from back.api.v1.setting.system import router as system
from back.api.v1.setting.user_quest_category import router as user_quest_category

router = APIRouter(prefix="/setting", tags=["Setting"])
router.include_router(front)
router.include_router(system)
router.include_router(user_quest_category)
