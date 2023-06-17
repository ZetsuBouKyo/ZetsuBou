from fastapi import APIRouter

from .minio import router as minio

router = APIRouter(prefix="/storage", tags=["Storage"])

router.include_router(minio)
