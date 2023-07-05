import json

from fastapi import HTTPException

from back.crud.async_gallery import CrudAsyncElasticsearchGallery
from back.db.crud import CrudUserElasticCountQuery


class CrudElasticCount:
    @classmethod
    async def count(cls, query_id: int) -> int:
        query = await CrudUserElasticCountQuery.get_row_by_id(query_id)
        if not query:
            raise HTTPException(
                status_code=404, detail=f"Elastic Count Query Id: {query_id} not found"
            )
        query_json = json.loads(query.query)

        crud = CrudAsyncElasticsearchGallery(is_from_setting_if_none=True)
        c = await crud.count(query_json["body"])
        return c.count
