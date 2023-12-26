import pytest

from back.db.crud import CrudGroup, CrudUser, CrudUserQuestCategory
from back.db.model import UserQuestCategoryEnum
from back.model.group import BuiltInGroupEnum
from back.security import verify_password
from back.security.group import builtin_groups
from back.settings import setting
from tests.general.session import DatabaseSession

ADMIN_GROUP_NAME = BuiltInGroupEnum.admin.value
GUEST_GROUP_NAME = BuiltInGroupEnum.guest.value

APP_ADMIN_EMAIL = setting.app_admin_email
APP_ADMIN_NAME = setting.app_admin_name
APP_ADMIN_PASSWORD = setting.app_admin_password

ELASTIC_COUNT_QUEST = UserQuestCategoryEnum.ELASTIC_COUNT_QUEST.value


async def check_groups_and_scopes():
    guest_group = await CrudGroup.get_row_with_scopes_by_name(GUEST_GROUP_NAME)
    assert guest_group is not None

    guest_scope_names = builtin_groups.get(GUEST_GROUP_NAME, None)
    assert guest_scope_names is not None
    assert set(guest_group.scope_names) == set(guest_scope_names)

    admin_group = await CrudGroup.get_row_with_scopes_by_name(ADMIN_GROUP_NAME)
    assert admin_group is not None

    admin_scope_names = builtin_groups.get(ADMIN_GROUP_NAME, None)
    assert admin_scope_names is not None
    assert set(admin_group.scope_names) == set(admin_scope_names)


async def check_admin_user():
    admin_user = await CrudUser.get_row_with_hashed_password_by_email(APP_ADMIN_EMAIL)
    assert admin_user is not None
    assert admin_user.name == APP_ADMIN_NAME
    assert verify_password(APP_ADMIN_PASSWORD, admin_user.hashed_password)


async def check_quest():
    category = await CrudUserQuestCategory.get_row_by_name(ELASTIC_COUNT_QUEST)
    assert category is not None


@pytest.mark.asyncio
async def test_initialization():
    async with DatabaseSession():
        await check_groups_and_scopes()
        await check_admin_user()
        await check_quest()
