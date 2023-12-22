from uuid import uuid4

import pytest

from back.db.crud import CrudTagCategory, CrudTagToken
from back.db.model import TagCategoryCreate, TagTokenCreate, TagTokenUpdate
from tests.general.session import SQLiteSession


@pytest.mark.asyncio
async def test_crud():
    async with SQLiteSession():
        token_total_0 = await CrudTagToken.count_total()

        # create category token
        token_name_1 = str(uuid4())
        token_1 = TagTokenCreate(name=token_name_1)
        token_1_created = await CrudTagToken.create(token_1)

        # create token
        token_name_2 = str(uuid4())
        token_2 = TagTokenCreate(name=token_name_2)
        token_2_created = await CrudTagToken.create(token_2)

        token_name_2_to_update = str(uuid4())
        token_2_to_update = TagTokenUpdate(
            id=token_2_created.id, name=token_name_2_to_update
        )
        await CrudTagToken.update_by_id(token_2_to_update)
        token_2_updated = await CrudTagToken.get_row_by_id(token_2_created.id)
        assert token_2_updated.id == token_2_created.id
        assert token_2_updated.name == token_name_2_to_update

        # test `CrudTagCategory.delete_by_id(...)`
        category_1 = TagCategoryCreate(
            linked_id=token_1_created.id, token_id=token_2_created.id
        )
        category_1_created = await CrudTagCategory.create(category_1)
        await CrudTagCategory.delete_by_id(category_1_created.id)
        category_1_deleted = await CrudTagCategory.get_row_by_id(category_1_created.id)
        assert category_1_deleted is None

        category_2 = TagCategoryCreate(
            linked_id=token_1_created.id, token_id=token_2_created.id
        )
        category_2_created = await CrudTagCategory.create(category_2)

        token_total_1 = await CrudTagToken.count_total()
        assert token_total_1 == token_total_0 + 2

        token_1_existed = await CrudTagToken.exists(token_1_created.id)
        assert token_1_existed is True

        token_1_by_id = await CrudTagToken.get_row_by_id(token_1_created.id)
        assert token_1_by_id is not None

        tokens = await CrudTagToken.get_rows_order_by_id()
        assert len(tokens) > 0

        ids = [token_1_created.id]
        tokens_by_ids = await CrudTagToken.get_rows_by_ids_order_by_id(ids)
        assert len(tokens_by_ids) == 1

        tokens_startswith = await CrudTagToken.startswith(token_name_1)
        assert len(tokens_startswith) == 1

        tokens_startswith_by_category = await CrudTagToken.startswith_by_category(
            "", token_name_1
        )
        assert len(tokens_startswith_by_category) == 1

        tokens_startswith_by_category_id = await CrudTagToken.startswith_by_category_id(
            "", token_1_created.id
        )
        assert len(tokens_startswith_by_category_id) == 1

        await CrudTagToken.delete_by_id(token_1_created.id)
        token_1_deleted = await CrudTagToken.get_row_by_id(token_1_created.id)
        assert token_1_deleted is None

        category_2_deleted = await CrudTagCategory.get_row_by_id(category_2_created.id)
        assert category_2_deleted is None

        await CrudTagToken.delete_by_id(token_2_created.id)
        token_2_deleted = await CrudTagToken.get_row_by_id(token_2_created.id)
        assert token_2_deleted is None
