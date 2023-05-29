from typing import List
from urllib.parse import unquote

from back.db.crud import CrudTagToken
from back.db.model import TagToken, TagTokenCreate, TagTokenCreated, TagTokenUpdate
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


@router.get(
    "/token-startswith",
    response_model=List[TagToken],
    dependencies=[api_security([ScopeEnum.tag_token_startswith_get.name])],
)
async def start_with(
    s: str = "",
    category: str = None,
    category_id: int = None,
    pagination: Pagination = Depends(get_pagination),
) -> List[TagToken]:
    s = unquote(s)
    s = s.lower()
    if category is not None:
        if category_id is not None:
            raise HTTPException(
                status_code=409, detail="category and category_id should choose one"
            )
        return await CrudTagToken.startwith_by_category(
            s,
            category,
            skip=pagination.skip,
            limit=pagination.size,
            is_desc=pagination.is_desc,
        )
    if category_id is None:
        return await CrudTagToken.startwith(
            s, skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
        )
    return await CrudTagToken.startwith_by_category_id(
        s,
        category_id,
        skip=pagination.skip,
        limit=pagination.size,
        is_desc=pagination.is_desc,
    )


@router.get(
    "/total-tokens",
    response_model=int,
    dependencies=[api_security([ScopeEnum.tag_toal_tokens_get.name])],
)
async def count_total_tokens() -> int:
    return await CrudTagToken.count_total()


@router.get(
    "/token/{token_id}/exists",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_token_exists_get.name])],
)
async def token_exists(token_id: int) -> bool:
    return await CrudTagToken.exists(token_id)


@router.get(
    "/token/{token_id}", dependencies=[api_security([ScopeEnum.tag_token_get.name])]
)
async def get_token():
    # TODO:
    return


@router.get(
    "/tokens",
    response_model=List[TagToken],
    dependencies=[api_security([ScopeEnum.tag_tokens_get.name])],
)
async def get_tokens(
    pagination: Pagination = Depends(get_pagination),
) -> List[TagToken]:
    return await CrudTagToken.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/token",
    response_model=TagTokenCreated,
    dependencies=[api_security([ScopeEnum.tag_token_post.name])],
)
async def post_token(token: TagTokenCreate) -> TagTokenCreated:
    return await CrudTagToken.create(token)


@router.put(
    "/token",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_token_put.name])],
)
async def put_token(token: TagTokenUpdate) -> bool:
    return await CrudTagToken.update_by_id(token)


@router.delete(
    "/token/{token_id}", dependencies=[api_security([ScopeEnum.tag_token_delete.name])]
)
async def delete_token(token_id: int) -> bool:
    # TODO: Delete token in elasticsearch
    return await CrudTagToken.delete_by_id(token_id)
