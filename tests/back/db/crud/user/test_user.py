from logging import Logger
from typing import Union
from unittest import TestCase

import pytest
from faker import Faker
from pydantic import ValidationError

from back.db.crud import CrudGroup, CrudUser, CrudUserFrontSettings
from back.db.crud.user.front_settings import _parameters
from back.db.model import UserWithGroupsCreate, UserWithGroupsUpdate
from back.model.group import BuiltInGroupEnum
from back.security import verify_password
from back.settings import setting

ADMIN_GROUP_NAME = BuiltInGroupEnum.admin.value
GUEST_GROUP_NAME = BuiltInGroupEnum.guest.value


async def assert_user(user: Union[UserWithGroupsCreate, UserWithGroupsUpdate]):
    created_user = await CrudUser.get_row_with_hashed_password_by_email(user.email)

    assert user.name == created_user.name
    assert user.email == created_user.email
    if type(user) == UserWithGroupsUpdate and user.new_password is not None:
        assert verify_password(user.new_password, created_user.hashed_password)
    else:
        assert verify_password(user.password, created_user.hashed_password)

    created_user_with_groups = await CrudUser.get_row_with_groups_by_id(created_user.id)

    TestCase().assertCountEqual(user.group_ids, created_user_with_groups.group_ids)

    # assert user front settings
    default_settings = setting.get_app_user_front_settings(created_user.id)
    default_setting_keys = [para.get("front_settings_key") for para in _parameters]
    user_front_settings = await CrudUserFrontSettings.get_row_by_user_id(
        created_user.id
    )
    user_front_settings = user_front_settings.model_dump()

    for key in default_setting_keys:
        default_setting = default_settings.get(key, None)
        if default_setting is None:
            continue

        user_front_setting = user_front_settings.get(key, None)
        if user_front_setting is None:
            continue

        assert default_setting == user_front_setting


async def update_user_with_groups(user_id: int, user: UserWithGroupsUpdate):
    await CrudUser.update_by_user_with_group(user_id, user)
    await assert_user(user)


@pytest.mark.asyncio
async def test_crud(init_sqlite: None, logger: Logger):
    admin_group = await CrudGroup.get_row_with_scopes_by_name(ADMIN_GROUP_NAME)
    guest_group = await CrudGroup.get_row_with_scopes_by_name(GUEST_GROUP_NAME)

    fake = Faker()
    name = fake.name()
    email = fake.email()
    password = fake.password()

    logger.info(f"name: {name}")
    logger.info(f"email: {email}")
    logger.info(f"password: {password}")

    user_with_groups_1 = UserWithGroupsCreate(
        name=name, email=email, password=password, group_ids=[admin_group.id]
    )

    created_user_with_groups_1 = await CrudUser.create_with_groups(user_with_groups_1)
    user_id_1 = created_user_with_groups_1.id
    await assert_user(user_with_groups_1)

    user_with_groups_1_to_update_1 = UserWithGroupsUpdate(
        name=user_with_groups_1.name,
        email=user_with_groups_1.email,
        password=user_with_groups_1.password,
        group_ids=[admin_group.id, guest_group.id],
    )
    await update_user_with_groups(user_id_1, user_with_groups_1_to_update_1)

    new_name = fake.name()
    new_password = fake.password()
    user_with_groups_1_to_update_2 = UserWithGroupsUpdate(
        name=new_name,
        email=user_with_groups_1.email,
        password=user_with_groups_1.password,
        new_password=new_password,
        group_ids=[],
    )
    await update_user_with_groups(user_id_1, user_with_groups_1_to_update_2)

    try:
        UserWithGroupsUpdate(
            name=new_name,
            email=user_with_groups_1.email,
            password=None,
            group_ids=[],
        )
        assert False
    except ValidationError:
        ...

    try:
        UserWithGroupsUpdate(
            name=new_name,
            email=user_with_groups_1.email,
            group_ids=[],
        )
        assert False
    except ValidationError:
        ...

    await CrudUser.delete_by_id(user_id_1)
    deleted_user_1 = await CrudUser.get_row_by_id(user_id_1)
    assert deleted_user_1 is None