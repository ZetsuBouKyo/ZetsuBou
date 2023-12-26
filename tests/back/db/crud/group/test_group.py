import pytest
from faker import Faker
from fastapi import HTTPException

from back.db.crud import CrudGroup, CrudScope
from back.db.model import (
    GroupCreate,
    GroupUpdate,
    GroupWithScopeIdsSafeCreate,
    GroupWithScopeIdsUpdate,
)
from back.model.group import BuiltInGroupEnum
from back.model.scope import ScopeEnum
from tests.general.logger import logger
from tests.general.session import DatabaseSession


@pytest.mark.asyncio
async def test_crud():
    faker = Faker()
    async with DatabaseSession():
        group_name_1 = faker.name()
        group_1 = GroupCreate(name=group_name_1)

        total_0 = await CrudGroup.count_total()
        group_1_created = await CrudGroup.create(group_1)
        total_1 = await CrudGroup.count_total()
        assert total_1 == total_0 + 1

        logger.info(f"ID: {group_1_created.id}")
        logger.info(f"name: {group_name_1}")

        groups_1 = await CrudGroup.get_rows_order_by_id()
        assert len(groups_1) > 0

        group_name_1_to_update = faker.name()
        logger.info(f"new name: {group_name_1}")
        group_1_to_update = GroupUpdate(
            id=group_1_created.id, name=group_name_1_to_update
        )
        await CrudGroup.update_by_id(group_1_to_update)
        group_1_updated = await CrudGroup.get_row_by_id(group_1_created.id)
        assert group_1_updated.name == group_name_1_to_update

        group_1_by_name = await CrudGroup.get_row_by_name(group_name_1_to_update)
        assert group_1_by_name is not None
        assert group_1_by_name.id == group_1_created.id
        assert group_1_by_name.name == group_name_1_to_update

        await CrudGroup.delete_by_id(group_1_created.id)
        group_1_deleted = await CrudGroup.get_row_by_id(group_1_created.id)
        assert group_1_deleted is None


@pytest.mark.asyncio
async def test_crud_with_scope_ids():
    faker = Faker()
    async with DatabaseSession():
        group_name_1 = faker.name()
        logger.info(f"name: {group_name_1}")

        scope_1 = await CrudScope.get_row_by_name(
            ScopeEnum.elasticsearch_analyzers_get.value
        )
        scope_2 = await CrudScope.get_row_by_name(
            ScopeEnum.elasticsearch_query_examples_get.value
        )

        group_1 = GroupWithScopeIdsSafeCreate(
            name=group_name_1, scope_ids=[scope_1.id, scope_2.id]
        )
        group_1_created = await CrudGroup.safe_create_with_scope_ids(group_1)
        assert set(group_1_created.scope_ids) == set([scope_1.id, scope_2.id])

        group_name_1_to_update = faker.name()
        logger.info(f"new name: {group_name_1_to_update}")

        group_1_to_update = GroupWithScopeIdsUpdate(
            id=group_1_created.id, name=group_name_1_to_update, scope_ids=[scope_1.id]
        )
        await CrudGroup.update_with_scope_ids_by_id(group_1_to_update)
        group_1_updated = await CrudGroup.get_row_with_scopes_by_id(group_1_created.id)
        assert group_1_updated.name == group_name_1_to_update
        assert set(group_1_updated.scope_ids) == set([scope_1.id])

        group_1_to_update_2 = GroupWithScopeIdsUpdate(
            id=group_1_created.id,
            name=group_name_1_to_update,
            scope_ids=[scope_1.id, scope_2.id],
        )
        await CrudGroup.update_with_scope_ids_by_id(group_1_to_update_2)
        group_1_by_name = await CrudGroup.get_row_with_scopes_by_name(
            group_1_updated.name
        )
        assert set(group_1_by_name.scope_ids) == set([scope_1.id, scope_2.id])

        await CrudGroup.delete_by_id(group_1_by_name.id)
        group_1_deleted = await CrudGroup.get_row_by_id(group_1_by_name.id)
        assert group_1_deleted is None


@pytest.mark.asyncio
async def test_init():
    async with DatabaseSession():
        total_0 = await CrudGroup.count_total()
        await CrudGroup.init()
        total_1 = await CrudGroup.count_total()
        assert total_0 == total_1

        groups_all = await CrudGroup.get_all_rows_order_by_id()
        assert len(groups_all) == total_1


@pytest.mark.asyncio
async def test_exception():
    async with DatabaseSession():
        with pytest.raises(HTTPException):
            admin_group = await CrudGroup.get_row_by_name(BuiltInGroupEnum.admin.value)
            await CrudGroup.delete_by_id(admin_group.id)
