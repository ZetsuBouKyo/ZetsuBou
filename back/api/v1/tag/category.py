from typing import List

from fastapi import APIRouter, Depends, HTTPException

from back.db.crud import CrudTagCategory, CrudTagToken
from back.db.model import TagCategory, TagCategoryCreate, TagCategoryCreated
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(prefix="/tag", tags=["Tag Category"])


@router.get(
    "/categories",
    response_model=List[TagCategory],
    dependencies=[api_security([ScopeEnum.tag_categories_get.name])],
)
async def get_tag_categories(
    pagination: Pagination = Depends(get_pagination),
) -> List[TagCategory]:
    return await CrudTagCategory.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/category",
    response_model=TagCategoryCreated,
    dependencies=[api_security([ScopeEnum.tag_category_post.name])],
)
async def post_tag_category(category: TagCategoryCreate) -> TagCategoryCreated:
    if category.linked_id == category.token_id:
        raise HTTPException(
            status_code=409,
            detail=f"Conflict between token id: {category.linked_id} and "
            f"{category.token_id}",
        )
    if await CrudTagToken.exists(category.linked_id) is None:
        raise HTTPException(
            status_code=404, detail=f"Token id: {category.linked_id} not found"
        )
    if await CrudTagToken.exists(category.token_id) is None:
        raise HTTPException(
            status_code=404, detail=f"Token id: {category.token_id} not found"
        )
    return await CrudTagCategory.create(category)


@router.delete(
    "/category/{id}", dependencies=[api_security([ScopeEnum.tag_category_delete.name])]
)
async def delete_tag_category(id: int):
    return await CrudTagCategory.delete_by_id(id)
