from typing import List

from ..model import Scope
from ..table import ScopeBase
from .base import get_all_rows_by_condition_order_by_id, get_rows_order_by_id


class CrudScope(ScopeBase):
    @classmethod
    async def get_rows_order_by_id(
        cls, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[Scope]:
        return await get_rows_order_by_id(
            cls, Scope, skip=skip, limit=limit, is_desc=is_desc
        )

    @classmethod
    async def get_all_rows_by_group_id_order_by_id(cls, group_id: int) -> List[Scope]:
        return await get_all_rows_by_condition_order_by_id(
            cls, cls.group_id == group_id, model=Scope
        )
