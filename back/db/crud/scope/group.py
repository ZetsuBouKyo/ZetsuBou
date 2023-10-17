from typing import List

from ...table import ScopeGroupBase
from ..base import get_all_rows_order_by_id


class CrudScopeGroup(ScopeGroupBase):
    @classmethod
    async def get_all_rows_order_by_id(cls) -> List[dict]:
        return await get_all_rows_order_by_id(cls)
