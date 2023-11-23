import json
from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.sql import functions as func

from ....model import (
    UserElasticSearchQuery,
    UserElasticSearchQueryCreate,
    UserElasticSearchQueryCreated,
    UserElasticSearchQueryUpdate,
)
from ....table import UserElasticSearchQueryBase
from ...base import (
    count,
    create,
    delete_by,
    get_row_by,
    get_row_by_id,
    get_rows_by_condition_order_by,
    update_by_id,
)


class CrudUserElasticSearchQuery(UserElasticSearchQueryBase):
    @classmethod
    async def create(cls, query: UserElasticSearchQueryCreate):
        json.loads(query.query)
        return UserElasticSearchQueryCreated(**await create(cls, query))

    @classmethod
    async def count_by_user_id(cls, user_id: int) -> int:
        return await count(cls, cls.user_id == user_id)

    @classmethod
    async def get_row_by_id(cls, id: int) -> Optional[UserElasticSearchQuery]:
        return await get_row_by_id(cls, id, UserElasticSearchQuery)

    @classmethod
    async def get_row_by_id_and_user_id(
        cls, id: int, user_id: int
    ) -> Optional[UserElasticSearchQuery]:
        return await get_row_by(
            cls, and_(cls.id == id, cls.user_id == user_id), UserElasticSearchQuery
        )

    @classmethod
    async def get_rows_by_user_id_order_by_id(
        cls, user_id: int, skip: int = 0, limit: int = 100, is_desc: bool = False
    ) -> List[UserElasticSearchQuery]:
        return await get_rows_by_condition_order_by(
            cls,
            cls.user_id == user_id,
            cls.id,
            UserElasticSearchQuery,
            skip,
            limit,
            is_desc,
        )

    @classmethod
    async def update_by_id(cls, query: UserElasticSearchQueryUpdate):
        json.loads(query.query)
        query = query.model_dump()
        query["modified"] = func.now()
        return await update_by_id(cls, query)

    @classmethod
    async def delete_by_id_and_user_id(cls, id: int, user_id: int):
        return await delete_by(cls, and_(cls.id == id, cls.user_id == user_id))
