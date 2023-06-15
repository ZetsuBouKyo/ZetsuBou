from fastapi import APIRouter

from .init import router as init

router = APIRouter(prefix="/v1", tags=["API"])

router.include_router(init)
