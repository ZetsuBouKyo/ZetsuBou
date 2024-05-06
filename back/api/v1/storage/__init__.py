from fastapi import APIRouter

from .minio import router as _minio

router = APIRouter(prefix="/storage", tags=["Storage"])

router.include_router(_minio)
