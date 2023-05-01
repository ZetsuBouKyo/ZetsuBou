from fastapi import APIRouter

from .front import router as front

router = APIRouter()

router.include_router(front, prefix="/front")
