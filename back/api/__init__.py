from fastapi import APIRouter

from back.api.v1 import router as _v1

router = APIRouter()


router.include_router(_v1, tags=["API"], prefix="/v1")
