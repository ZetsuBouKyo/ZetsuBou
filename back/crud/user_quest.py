import json

from back.crud.gallery import CrudElasticGallery
from back.db.crud import CrudUserElasticCountQuery
from fastapi import HTTPException


class CrudElasticCount:
    @classmethod
    async def count(cls, query_id: int) -> int:
        query = await CrudUserElasticCountQuery.get_row_by_id(query_id)
        if not query:
            raise HTTPException(
                status_code=404, detail=f"Elastic Count Query Id: {query_id} not found"
            )
        query_json = json.loads(query.query)

        crud_es = CrudElasticGallery()
        return crud_es.count(query_json["body"]).count
