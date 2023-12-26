from uuid import uuid4

import pytest

from back.db.crud import CrudTagAttribute
from back.db.model import TagAttributeCreate, TagAttributeUpdate
from tests.general.logger import logger
from tests.general.session import SQLiteSession


@pytest.mark.asyncio
async def test_crud():
    async with SQLiteSession():
        attr_name_1 = str(uuid4())[:8]
        attr_total_0 = await CrudTagAttribute.count_total()
        logger.info(f"attribute: {attr_name_1}")
        logger.info(f"total: {attr_total_0}")

        attr_1 = TagAttributeCreate(name=attr_name_1)
        attr_1_created = await CrudTagAttribute.create(attr_1)
        assert attr_1_created.name == attr_name_1

        attr_total_1 = await CrudTagAttribute.count_total()
        assert attr_total_1 == (attr_total_0 + 1)

        attr_1_by_id = await CrudTagAttribute.get_row_by_id(attr_1_created.id)
        assert attr_1_by_id.id == attr_1_created.id
        assert attr_1_by_id.name == attr_name_1

        attr_1_by_name = await CrudTagAttribute.get_row_by_name(attr_1_created.name)
        assert attr_1_by_name.id == attr_1_created.id
        assert attr_1_by_name.name == attr_name_1

        attrs = await CrudTagAttribute.get_rows_order_by_id()
        assert len(attrs) > 0

        attr_name_1_to_update = str(uuid4())[:8]
        logger.info(f"attribute (to update): {attr_name_1_to_update}")

        attr_1_to_update = TagAttributeUpdate(
            id=attr_1_created.id, name=attr_name_1_to_update
        )
        await CrudTagAttribute.update_by_id(attr_1_to_update)
        attr_1_updated = await CrudTagAttribute.get_row_by_id(attr_1_created.id)

        assert attr_1_updated.id == attr_1_created.id
        assert attr_1_updated.name == attr_name_1_to_update

        await CrudTagAttribute.delete_by_id(attr_1_created.id)
        attr_1_deleted = await CrudTagAttribute.get_row_by_id(attr_1_created.id)
        assert attr_1_deleted is None
