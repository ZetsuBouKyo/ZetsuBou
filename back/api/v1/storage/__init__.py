from fastapi import APIRouter

from .minio import router as minio

router = APIRouter()
router.include_router(minio, tags=["Minio Storage"], prefix="/minio")
