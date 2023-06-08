from typing import List, Union

from back.db.crud import CrudUserBookmarkGallery
from back.db.model import (
    UserBookmarkGallery,
    UserBookmarkGalleryCreate,
    UserBookmarkGalleryCreated,
    UserBookmarkGalleryUpdate,
)
from back.dependency.security import api_security
from back.model.scope import ScopeEnum
from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/{user_id}/bookmark/galleries",
    response_model=List[UserBookmarkGallery],
    dependencies=[api_security([ScopeEnum.user_bookmark_galleries_get.name])],
)
async def get_gallery_bookmarks(user_id: int) -> List[UserBookmarkGallery]:
    return await CrudUserBookmarkGallery.get_rows_by_user_id(user_id)


@router.get(
    "/{user_id}/bookmark/gallery/g/{gallery_id}",
    response_model=Union[UserBookmarkGallery, None],
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_get.name])],
)
async def get_gallery_bookmark(user_id: int, gallery_id: str) -> UserBookmarkGallery:
    return await CrudUserBookmarkGallery.get_row_by_user_id_and_gallery_id(
        user_id, gallery_id
    )


@router.post(
    "/{user_id}/bookmark/gallery",
    response_model=UserBookmarkGalleryCreated,
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_post.name])],
)
async def post_gallery_bookmark(
    bookmark: UserBookmarkGalleryCreate,
) -> UserBookmarkGalleryCreated:
    return await CrudUserBookmarkGallery.create(bookmark)


@router.put(
    "/{user_id}/bookmark/gallery",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_put.name])],
)
async def put_gallery_bookmark(
    bookmark: UserBookmarkGalleryUpdate,
) -> bool:
    return await CrudUserBookmarkGallery.update_by_id(bookmark)


@router.delete(
    "/{user_id}/bookmark/gallery/b/{bookmark_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_delete.name])],
)
async def delete_gallery_bookmark(bookmark_id: int) -> bool:
    return await CrudUserBookmarkGallery.delete_by_id(bookmark_id)
