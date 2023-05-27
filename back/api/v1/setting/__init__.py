from fastapi import APIRouter

from .front import router as front
from .user_quest_category import router as user_quest_category

router = APIRouter()

router.include_router(front, prefix="/front")
router.include_router(user_quest_category)
