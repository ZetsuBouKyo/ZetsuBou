from typing import List

from ...model import Scope, ScopeCreate, ScopeCreated
from ...table import ScopeBase
from ..base import create, get_rows_order_by_id


class CrudScope(ScopeBase):
    @classmethod
    async def create(cls, token: ScopeCreate) -> ScopeCreated:
        return ScopeCreated(**await create(cls, token))

    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[Scope]:
        return await get_rows_order_by_id(
            cls, Scope, skip=skip, limit=limit, is_desc=is_desc
        )
