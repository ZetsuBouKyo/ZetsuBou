from logging import Logger
from uuid import uuid4

import pytest

from back.db.crud import CrudUserBookmarkGallery
from back.db.model import UserBookmarkGalleryCreate, UserBookmarkGalleryUpdate
from tests.general.user import UserSession


@pytest.mark.asyncio
async def test_crud(logger: Logger):
    async with UserSession() as session:
        user = session.created_user_with_groups
        gallery_id_1 = str(uuid4())

        logger.info(f"gallery ID: {gallery_id_1}")

        bookmark_1 = UserBookmarkGalleryCreate(
            user_id=user.id, gallery_id=gallery_id_1, page=1
        )
        bookmark_1_1 = await CrudUserBookmarkGallery.create(bookmark_1)

        total = await CrudUserBookmarkGallery.count_total_by_user_id(user.id)
        assert total == 1

        bookmarks_1_1 = await CrudUserBookmarkGallery.get_rows_by_user_id(user.id)
        assert len(bookmarks_1_1) == 1

        bookmarks_1_2 = (
            await CrudUserBookmarkGallery.get_rows_by_user_id_order_by_modified(user.id)
        )
        assert len(bookmarks_1_2) == 1

        page = 2
        bookmark_1_2 = UserBookmarkGalleryUpdate(
            id=bookmark_1_1.id, user_id=user.id, gallery_id=gallery_id_1, page=page
        )
        await CrudUserBookmarkGallery.update_by_id(bookmark_1_2)

        bookmark_1_2_1 = (
            await CrudUserBookmarkGallery.get_row_by_user_id_and_gallery_id(
                user.id, gallery_id_1
            )
        )
        assert bookmark_1_2_1.gallery_id == gallery_id_1
        assert bookmark_1_2_1.page == page

    bookmarks_1_1 = await CrudUserBookmarkGallery.get_rows_by_user_id(user.id)
    assert len(bookmarks_1_1) == 0
