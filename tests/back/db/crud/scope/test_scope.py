from enum import Enum

import pytest

from back.db.crud import CrudScope
from back.db.model import ScopeCreate, ScopeUpdate
from back.model.scope import ScopeEnum
from back.utils.enum import StrEnumMeta
from tests.general.session import DatabaseSession


@pytest.mark.asyncio
@pytest.mark.integration
async def test_crud():
    async with DatabaseSession():
        scopes_all = await CrudScope.get_all_rows_order_by_id()
        scopes = await CrudScope.get_rows_order_by_id()
        assert len(scopes) > 0
        assert len(scopes_all) == len(ScopeEnum)

        scope_name_1 = "tests scope 1"
        scope_1 = ScopeCreate(name=scope_name_1)
        scope_1_created = await CrudScope.create(scope_1)

        scope_name_1_to_update = "tests scope 2"
        scope_1_to_update = ScopeUpdate(
            id=scope_1_created.id, name=scope_name_1_to_update
        )
        await CrudScope.update_by_id(scope_1_to_update)
        scope_1_updated = await CrudScope.get_row_by_id(scope_1_created.id)
        assert scope_1_updated.id == scope_1_created.id
        assert scope_1_updated.name == scope_name_1_to_update

        scope_1_startswith = await CrudScope.startswith(scope_name_1_to_update)
        assert len(scope_1_startswith) > 0

        await CrudScope.delete_by_id(scope_1_created.id)
        scope_1_deleted = await CrudScope.get_row_by_id(scope_1_created.id)
        assert scope_1_deleted is None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_init():
    async with DatabaseSession():

        class ScopeEnumPlus(str, Enum, metaclass=StrEnumMeta):
            tests: str = "tests plus"

        await CrudScope.init(scope_enum=ScopeEnumPlus)
        scope = await CrudScope.get_row_by_name(ScopeEnumPlus.tests.value)
        assert scope is not None

        await CrudScope.delete_by_id(scope.id)
        scope_deleted = await CrudScope.get_row_by_id(scope.id)
        assert scope_deleted is None
