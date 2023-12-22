from uuid import uuid4

import pytest

from back.db.crud import CrudUserBookmarkGallery
from back.db.model import UserBookmarkGalleryCreate, UserBookmarkGalleryUpdate
from tests.general.logger import logger
from tests.general.session import UserSession


@pytest.mark.asyncio
async def test_crud():
    async with UserSession() as session:
        user = session.created_user_with_groups

        gallery_id_1 = str(uuid4())
        logger.info(f"gallery ID: {gallery_id_1}")

        bookmark_1 = UserBookmarkGalleryCreate(
            user_id=user.id, gallery_id=gallery_id_1, page=1
        )
        bookmark_1_created = await CrudUserBookmarkGallery.create(bookmark_1)

        total = await CrudUserBookmarkGallery.count_total_by_user_id(user.id)
        assert total == 1

        bookmarks_1 = await CrudUserBookmarkGallery.get_rows_by_user_id(user.id)
        assert len(bookmarks_1) == 1

        bookmarks_1_2 = (
            await CrudUserBookmarkGallery.get_rows_by_user_id_order_by_modified(user.id)
        )
        assert len(bookmarks_1_2) == 1

        page_1_to_update = 2
        bookmark_1_to_update = UserBookmarkGalleryUpdate(
            id=bookmark_1_created.id,
            user_id=user.id,
            gallery_id=gallery_id_1,
            page=page_1_to_update,
        )
        await CrudUserBookmarkGallery.update_by_id(bookmark_1_to_update)

        bookmark_1_updated = (
            await CrudUserBookmarkGallery.get_row_by_user_id_and_gallery_id(
                user.id, gallery_id_1
            )
        )
        assert bookmark_1_updated.gallery_id == gallery_id_1
        assert bookmark_1_updated.page == page_1_to_update

        gallery_id_2 = str(uuid4())
        logger.info(f"gallery ID: {gallery_id_2}")

        bookmark_2 = UserBookmarkGalleryCreate(
            user_id=user.id, gallery_id=gallery_id_2, page=1
        )
        bookmark_2_created = await CrudUserBookmarkGallery.create(bookmark_2)
        await CrudUserBookmarkGallery.delete_by_id(bookmark_2_created.id)
        bookmark_2_deleted = (
            await CrudUserBookmarkGallery.get_row_by_user_id_and_gallery_id(
                user.id, gallery_id_2
            )
        )
        assert bookmark_2_deleted is None

    bookmarks_2 = await CrudUserBookmarkGallery.get_rows_by_user_id(user.id)
    assert len(bookmarks_2) == 0
