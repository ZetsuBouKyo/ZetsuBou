from typing import List

from fastapi import APIRouter, Depends

from back.db.crud import CrudTagAttribute
from back.db.model import (
    TagAttribute,
    TagAttributeCreate,
    TagAttributeCreated,
    TagAttributeUpdate,
)
from back.dependency.base import get_pagination
from back.dependency.security import api_security
from back.model.base import Pagination
from back.model.scope import ScopeEnum

router = APIRouter(prefix="/tag", tags=["Tag Attribute"])


@router.get(
    "/total-attributes",
    response_model=int,
    dependencies=[api_security([ScopeEnum.tag_total_attributes_get.value])],
)
async def count_total_attributes() -> int:
    return await CrudTagAttribute.count_total()


@router.get(
    "/attributes",
    response_model=List[TagAttribute],
    dependencies=[api_security([ScopeEnum.tag_attributes_get.value])],
)
async def get_attributes(
    pagination: Pagination = Depends(get_pagination),
) -> List[TagAttribute]:
    return await CrudTagAttribute.get_rows_order_by_id(
        skip=pagination.skip, limit=pagination.size, is_desc=pagination.is_desc
    )


@router.post(
    "/attribute",
    response_model=TagAttributeCreated,
    dependencies=[api_security([ScopeEnum.tag_attribute_post.value])],
)
async def post_attribute(attribute: TagAttributeCreate) -> TagAttributeCreated:
    return await CrudTagAttribute.create(attribute)


@router.put(
    "/attribute",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_attribute_put.value])],
)
async def put_attribute(attribute: TagAttributeUpdate) -> bool:
    return await CrudTagAttribute.update_by_id(attribute)


@router.delete(
    "/attribute/{attribute_id}",
    response_model=bool,
    dependencies=[api_security([ScopeEnum.tag_attribute_delete.value])],
)
async def delete_attribute(attribute_id: int) -> bool:
    # TODO: update elasticsearch
    return await CrudTagAttribute.delete_by_id(attribute_id)
