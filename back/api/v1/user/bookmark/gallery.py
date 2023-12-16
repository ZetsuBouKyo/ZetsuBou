from typing import List, Optional

from fastapi import APIRouter, Depends

from back.crud.async_gallery import CrudAsyncElasticsearchGallery
from back.db.crud import CrudUserBookmarkGallery
from back.db.model import (
    UserBookmarkGallery,
    UserBookmarkGalleryCreate,
    UserBookmarkGalleryCreated,
    UserBookmarkGalleryUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.bookmark import GalleryBookmark
from back.model.gallery import Galleries
from back.model.scope import ScopeEnum

router = APIRouter()


@router.get(
    "/{user_id}/total-bookmarks",
    response_model=int,
    dependencies=[api_security([ScopeEnum.user_total_bookmarks_get.value])],
)
async def count_total_bookmarks(user_id: int) -> int:
    return await CrudUserBookmarkGallery.count_total_by_user_id(user_id)


@router.get(
    "/{user_id}/bookmarks/gallery/detail",
    response_model=List[GalleryBookmark],
    dependencies=[api_security([ScopeEnum.user_bookmarks_gallery_detail_get.value])],
)
async def get_detailed_gallery_bookmarks(
    user_id: int, pagination: Pagination = Depends(get_pagination)
) -> List[GalleryBookmark]:
    bookmarks = await CrudUserBookmarkGallery.get_rows_by_user_id_order_by_modified(
        user_id, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )
    if len(bookmarks) == 0:
        return []

    gallery_ids = [bookmark.gallery_id for bookmark in bookmarks]

    async with CrudAsyncElasticsearchGallery(
        size=pagination.size, is_from_setting_if_none=True
    ) as elasticsearch_crud:
        _galleries = await elasticsearch_crud.get_sources_by_ids(gallery_ids)
        galleries = Galleries(**_galleries)
        galleries_table = {hit.source.id: hit.source for hit in galleries.hits.hits}
        detailed_bookmarks = [
            GalleryBookmark(
                bookmark=bookmark, gallery=galleries_table[bookmark.gallery_id]
            )
            for bookmark in bookmarks
        ]
    return detailed_bookmarks


@router.get(
    "/{user_id}/bookmarks/gallery",
    response_model=List[UserBookmarkGallery],
    dependencies=[api_security([ScopeEnum.user_bookmarks_gallery_get.value])],
)
async def get_gallery_bookmarks(
    user_id: int, pagination: Pagination = Depends(get_pagination)
) -> List[UserBookmarkGallery]:
    return await CrudUserBookmarkGallery.get_rows_by_user_id(
        user_id, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.get(
    "/{user_id}/bookmark/gallery/g/{gallery_id}",
    response_model=Optional[UserBookmarkGallery],
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_get.value])],
)
async def get_gallery_bookmark(user_id: int, gallery_id: str) -> UserBookmarkGallery:
    return await CrudUserBookmarkGallery.get_row_by_user_id_and_gallery_id(
        user_id, gallery_id
    )


@router.post(
    "/{user_id}/bookmark/gallery",
    response_model=UserBookmarkGalleryCreated,
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_post.value])],
)
async def post_gallery_bookmark(
    bookmark: UserBookmarkGalleryCreate,
) -> UserBookmarkGalleryCreated:
    return await CrudUserBookmarkGallery.create(bookmark)


@router.put(
    "/{user_id}/bookmark/gallery",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_put.value])],
)
async def put_gallery_bookmark(
    bookmark: UserBookmarkGalleryUpdate,
) -> bool:
    return await CrudUserBookmarkGallery.update_by_id(bookmark)


@router.delete(
    "/{user_id}/bookmark/gallery/b/{bookmark_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.user_bookmark_gallery_delete.value])],
)
async def delete_gallery_bookmark(bookmark_id: int) -> bool:
    return await CrudUserBookmarkGallery.delete_by_id(bookmark_id)
