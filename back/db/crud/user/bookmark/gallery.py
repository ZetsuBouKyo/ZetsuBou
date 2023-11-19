from typing import List

from sqlalchemy.sql import functions as func

from ....model import (
    UserBookmarkGallery,
    UserBookmarkGalleryCreate,
    UserBookmarkGalleryCreated,
    UserBookmarkGalleryUpdate,
)
from ....table import UserBookmarkGalleryBase
from ...base import (
    count,
    create,
    delete_by_id,
    get_row_by,
    get_rows_by_condition_order_by,
    get_rows_by_condition_order_by_id,
    update_by_id,
)


class CrudUserBookmarkGallery(UserBookmarkGalleryBase):
    @classmethod
    async def create(
        cls, bookmark: UserBookmarkGalleryCreate
    ) -> UserBookmarkGalleryCreated:
        created_bookmark = await create(cls, bookmark)
        return UserBookmarkGalleryCreated(**created_bookmark)

    @classmethod
    async def count_total_by_user_id(cls, user_id: int) -> int:
        return await count(cls, cls.user_id == user_id)

    @classmethod
    async def get_rows_by_user_id_order_by_modified(
        cls, user_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserBookmarkGallery]:
        return await get_rows_by_condition_order_by(
            cls,
            cls.user_id == user_id,
            cls.modified,
            UserBookmarkGallery,
            skip=skip,
            limit=limit,
            is_desc=is_desc,
        )

    @classmethod
    async def get_rows_by_user_id(
        cls, user_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserBookmarkGallery]:
        return await get_rows_by_condition_order_by_id(
            cls,
            cls.user_id == user_id,
            UserBookmarkGallery,
            skip=skip,
            limit=limit,
            is_desc=is_desc,
        )

    @classmethod
    async def get_row_by_user_id_and_gallery_id(
        cls, user_id: int, gallery_id: str
    ) -> UserBookmarkGallery:
        return await get_row_by(
            cls,
            (cls.user_id == user_id) & (cls.gallery_id == gallery_id),
            UserBookmarkGallery,
        )

    @classmethod
    async def update_by_id(cls, bookmark: UserBookmarkGalleryUpdate) -> bool:
        bookmark = bookmark.model_dump()
        bookmark["modified"] = func.now()
        return await update_by_id(cls, bookmark)

    @classmethod
    async def delete_by_id(cls, id: int) -> bool:
        return await delete_by_id(cls, id)
