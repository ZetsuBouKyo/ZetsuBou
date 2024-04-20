from fastapi import APIRouter

from back.api.v1.elasticsearch import router as elasticsearch
from back.api.v1.gallery import router as gallery
from back.api.v1.group import router as group
from back.api.v1.init import router as init
from back.api.v1.scope import router as scope
from back.api.v1.setting import router as setting
from back.api.v1.storage import router as storage
from back.api.v1.tag import router as tag
from back.api.v1.task import router as task
from back.api.v1.token import router as token
from back.api.v1.user import router as user
from back.api.v1.users import router as users
from back.api.v1.video import router as video

router = APIRouter()

router.include_router(init)
router.include_router(token)

router.include_router(user)
router.include_router(users)
router.include_router(group)
router.include_router(scope)
router.include_router(setting)
router.include_router(task)
router.include_router(tag)

router.include_router(gallery)
router.include_router(video)

router.include_router(elasticsearch)
router.include_router(storage)
