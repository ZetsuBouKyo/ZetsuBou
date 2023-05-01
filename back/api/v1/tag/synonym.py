from typing import List

from back.db.crud import CrudTagSynonym, CrudTagToken
from back.db.model import (
    ScopeEnum,
    TagSynonym,
    TagSynonymCreate,
    TagSynonymCreated,
    TagSynonymUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


async def verify_token_id(synonym):
    if await CrudTagToken.exists(synonym.linked_id) is None:
        raise HTTPException(
            status_code=404, detail=f"Token id: {synonym.linked_id} not found"
        )
    if await CrudTagToken.exists(synonym.token_id) is None:
        raise HTTPException(
            status_code=404, detail=f"Token id: {synonym.token_id} not found"
        )


@router.get(
    "/synonyms",
    response_model=List[TagSynonym],
    dependencies=[api_security([ScopeEnum.tag_synonyms_get.name])],
)
async def get_synonyms(
    pagination: Pagination = Depends(get_pagination),
) -> List[TagSynonym]:
    return await CrudTagSynonym.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/synonym",
    response_model=TagSynonymCreated,
    dependencies=[api_security([ScopeEnum.tag_synonym_post.name])],
)
async def post_synonym(synonym: TagSynonymCreate) -> TagSynonymCreated:
    await verify_token_id(synonym)
    return await CrudTagSynonym.create(synonym)


@router.put(
    "/synonym",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_synonym_put.name])],
)
async def put_synonym(synonym: TagSynonymUpdate) -> bool:
    await verify_token_id(synonym)
    return await CrudTagSynonym.update_by_id(synonym)


@router.delete(
    "/synonym/{id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_synonym_delete.name])],
)
async def delete_synonym(id: int) -> bool:
    return await CrudTagSynonym.delete_by_id(id)
