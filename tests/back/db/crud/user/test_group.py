from logging import Logger

import pytest

from back.db.crud import CrudGroup, CrudUserGroup
from back.db.model import UserGroupCreate
from back.model.group import BuiltInGroupEnum
from tests.general.db import SQLiteSession
from tests.general.user import UserSession

ADMIN_GROUP_NAME = BuiltInGroupEnum.admin.value
GUEST_GROUP_NAME = BuiltInGroupEnum.guest.value


@pytest.mark.asyncio
async def test_crud(logger: Logger):
    async with SQLiteSession():
        admin_group = await CrudGroup.get_row_with_scopes_by_name(ADMIN_GROUP_NAME)
        guest_group = await CrudGroup.get_row_with_scopes_by_name(GUEST_GROUP_NAME)

    async with UserSession() as session:
        user = session.created_user_with_groups

        user_group_id_1 = admin_group.id
        user_group_1 = UserGroupCreate(user_id=user.id, group_id=user_group_id_1)
        user_group_1_created = await CrudUserGroup.create(user_group_1)
        assert user_group_1_created.group_id == user_group_id_1

        user_group_id_1_to_update = guest_group.id
        await CrudUserGroup.update(user.id, [user_group_id_1_to_update])
        user_group_1_updated = await CrudUserGroup.get_row_by_id(
            user_group_1_created.id
        )
        assert user_group_1_updated.group_id == user_group_id_1_to_update

        user_groups_by_user_id = await CrudUserGroup.get_rows_by_user_id_order_by_id(
            user.id
        )
        assert len(user_groups_by_user_id) == 1

        user_groups_by_group_id = await CrudUserGroup.get_rows_by_group_id_order_by_id(
            user_group_id_1
        )

        assert len(user_groups_by_group_id) > 0

        user_groups = await CrudUserGroup.get_rows_order_by_id()
        assert len(user_groups) > 0

        await CrudUserGroup.delete_by_id(user_group_1_created.id)
        user_group_1_deleted = await CrudUserGroup.get_row_by_id(
            user_group_1_created.id
        )
        assert user_group_1_deleted is None
