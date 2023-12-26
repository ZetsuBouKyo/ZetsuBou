import pytest

from back.db.crud import CrudScopeGroup
from tests.general.session import DatabaseSession


@pytest.mark.asyncio
async def test_crud():
    async with DatabaseSession():
        links = await CrudScopeGroup.get_all_rows_order_by_id()
        assert len(links) > 0
