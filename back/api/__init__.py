from fastapi import APIRouter

from back.api.v1 import router as v1

router = APIRouter()


router.include_router(v1, tags=["API"], prefix="/v1")
