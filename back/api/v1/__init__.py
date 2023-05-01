from fastapi import APIRouter

from .elasticsearch import router as elasticsearch
from .gallery import router as gallery
from .group import router as group
from .minio import router as minio
from .setting import router as setting
from .sys import router as sys
from .tag import router as tag
from .task import router as task
from .token import router as token
from .user import router as user
from .users import router as users
from .video import router as video

router = APIRouter()

router.include_router(token, tags=["Token"], prefix="/token")

router.include_router(user, tags=["User"], prefix="/user")
router.include_router(users, tags=["Users"], prefix="/users")
router.include_router(group, tags=["Group"])
router.include_router(sys, tags=["System"], prefix="/sys")
router.include_router(setting, tags=["Setting"], prefix="/setting")
router.include_router(task, tags=["Task"], prefix="/task")
router.include_router(tag, tags=["Tag"])

router.include_router(gallery, tags=["Gallery"], prefix="/gallery")
router.include_router(video, tags=["Video"], prefix="/video")

router.include_router(elasticsearch, tags=["Elasticsearch"], prefix="/elasticsearch")
router.include_router(minio, tags=["Minio"], prefix="/minio")
