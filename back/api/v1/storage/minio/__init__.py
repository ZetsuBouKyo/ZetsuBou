from fastapi import APIRouter

from .operation import router as operation
from .storage import router as storage

router = APIRouter(prefix="/minio", tags=["Minio Storage"])
router.include_router(storage)
router.include_router(operation)
