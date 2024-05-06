from fastapi import APIRouter

from back.api.v1.setting.front import router as _front
from back.api.v1.setting.system import router as _system
from back.api.v1.setting.user_quest_category import router as _user_quest_category

router = APIRouter(prefix="/setting", tags=["Setting"])
router.include_router(_front)
router.include_router(_system)
router.include_router(_user_quest_category)
