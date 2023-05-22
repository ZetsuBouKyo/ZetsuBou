from fastapi import APIRouter

from .operation import router as operation
from .storage import router as storage

router = APIRouter()
router.include_router(storage, tags=["Minio Storage"])
router.include_router(operation, tags=["Minio Operation"])
