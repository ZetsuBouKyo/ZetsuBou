from typing import List

from back.crud.async_tag import CrudAsyncElasticsearchTag, CrudTag
from back.db.crud import CrudTagToken
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum
from back.model.tag import Tag, TagCreate, TagToken, TagUpdate
from fastapi import APIRouter, Depends

from .attribute import router as attribute
from .category import router as category
from .synonym import router as synonym
from .token import router as token

router = APIRouter()
router.include_router(attribute, tags=["Tag Attribute"], prefix="/tag")
router.include_router(category, tags=["Tag Category"], prefix="/tag")
router.include_router(synonym, tags=["Tag Synonym"], prefix="/tag")
router.include_router(token, tags=["Tag Token"], prefix="/tag")


@router.get(
    "/search-for-tag-attributes",
    response_model=List[TagToken],
    dependencies=[api_security([ScopeEnum.tag_search_for_tag_attributes_get.name])],
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
        return await CrudTagToken.get_rows_by_ids_order_by_id(ids)
    return []


@router.get(
    "/tag/{tag_id}/interpretation",
    response_model=Tag,
    dependencies=[api_security([ScopeEnum.tag_interpretation_get.name])],
)
async def get_interpretation_of_tag(tag_id: int) -> Tag:
    crud = CrudTag()
    return await crud.get_interpretation_by_id(tag_id)


@router.get(
    "/tag/{tag_id}",
    response_model=TagUpdate,
    dependencies=[api_security([ScopeEnum.tag_get.name])],
)
async def get_tag(tag_id: int) -> TagUpdate:
    crud = CrudTag()
    return await crud.get_row_by_id(tag_id)


@router.delete(
    "/tag/{tag_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_delete.name])],
)
async def delete_tag(tag_id: int) -> bool:
    crud = CrudTag()
    return await crud.delete_by_id(tag_id)


@router.post("/tag", dependencies=[api_security([ScopeEnum.tag_post.name])])
async def post_tag(tag: TagCreate):
    crud = CrudTag()
    return await crud.create(tag)


@router.put("/tag", dependencies=[api_security([ScopeEnum.tag_put.name])])
async def put_tag(tag: TagUpdate):
    crud = CrudTag()
    return await crud.update(tag)
