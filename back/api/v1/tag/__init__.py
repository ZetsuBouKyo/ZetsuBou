from typing import List, Optional

from fastapi import APIRouter, Depends

from back.crud.async_tag import CrudAsyncElasticsearchTag, CrudTag
from back.db.crud import CrudTagToken
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum
from back.model.tag import Tag, TagCreate, TagToken, TagUpdate

from .attribute import router as attribute
from .token import router as token

router = APIRouter(tags=["Tag"])
router.include_router(attribute)
router.include_router(token)


@router.get(
    "/search-for-tag-attributes",
    response_model=List[TagToken],
    dependencies=[api_security([ScopeEnum.tag_search_for_tag_attributes_get.value])],
)
async def search(
    s: str = "", pagination: Pagination = Depends(get_pagination)
) -> List[TagToken]:
    if not s:
        return []
    elastic_crud = CrudAsyncElasticsearchTag(size=pagination.size)
    results = await elastic_crud.match(pagination.page, s)
    ids = [int(r.id) for r in results.hits.hits]
    if len(ids) > 0:
        return await CrudTagToken.get_rows_by_ids_order_by_id(
            ids, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
        )
    return []


@router.get(
    "/tag/{tag_id}/interpretation",
    response_model=Optional[Tag],
    dependencies=[api_security([ScopeEnum.tag_interpretation_get.value])],
)
async def get_interpretation_of_tag(tag_id: int) -> Tag:
    crud = CrudTag()
    tag = await crud.get_interpretation_by_id(tag_id)
    return tag


@router.get(
    "/tag/{tag_id}",
    response_model=TagUpdate,
    dependencies=[api_security([ScopeEnum.tag_get.value])],
)
async def get_tag(tag_id: int) -> TagUpdate:
    crud = CrudTag()
    return await crud.get_row_by_id(tag_id)


@router.delete(
    "/tag/{tag_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_delete.value])],
)
async def delete_tag(tag_id: int) -> bool:
    crud = CrudTag()
    return await crud.delete_by_id(tag_id)


@router.post("/tag", dependencies=[api_security([ScopeEnum.tag_post.value])])
async def post_tag(tag: TagCreate):
    crud = CrudTag()
    return await crud.create(tag)


@router.put("/tag", dependencies=[api_security([ScopeEnum.tag_put.value])])
async def put_tag(tag: TagUpdate):
    crud = CrudTag()
    return await crud.update(tag)
