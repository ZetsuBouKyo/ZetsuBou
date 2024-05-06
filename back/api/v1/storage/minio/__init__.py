from fastapi import APIRouter

from .operation import router as _operation
from .storage import router as _storage

router = APIRouter(prefix="/minio", tags=["Minio Storage"])
router.include_router(_storage)
router.include_router(_operation)
