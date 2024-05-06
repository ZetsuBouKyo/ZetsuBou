from fastapi import APIRouter

from back.api.v1.elasticsearch import router as _elasticsearch
from back.api.v1.gallery import router as _gallery
from back.api.v1.group import router as _group
from back.api.v1.init import router as _init
from back.api.v1.scope import router as _scope
from back.api.v1.setting import router as _setting
from back.api.v1.storage import router as _storage
from back.api.v1.tag import router as _tag
from back.api.v1.task import router as _task
from back.api.v1.token import router as _token
from back.api.v1.user import router as _user
from back.api.v1.users import router as _users
from back.api.v1.video import router as _video

router = APIRouter()

router.include_router(_init)
router.include_router(_token)

router.include_router(_user)
router.include_router(_users)
router.include_router(_group)
router.include_router(_scope)
router.include_router(_setting)
router.include_router(_task)
router.include_router(_tag)

router.include_router(_gallery)
router.include_router(_video)

router.include_router(_elasticsearch)
router.include_router(_storage)
