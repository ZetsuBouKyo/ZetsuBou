from fastapi import APIRouter

from .elasticsearch import router as elasticsearch
from .gallery import router as gallery
from .group import router as group
from .init import router as init
from .setting import router as setting
from .storage import router as storage
from .tag import router as tag
from .task import router as task
from .token import router as token
from .user import router as user
from .users import router as users
from .video import router as video

router = APIRouter()

router.include_router(init)
router.include_router(token)

router.include_router(user)
router.include_router(users)
router.include_router(group)
router.include_router(setting)
router.include_router(task)
router.include_router(tag)

router.include_router(gallery)
router.include_router(video)

router.include_router(elasticsearch)
router.include_router(storage)
