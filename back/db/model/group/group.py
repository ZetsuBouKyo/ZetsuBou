from typing import List

from pydantic import BaseModel

from ..scope import ScopeEnum


class GroupCreate(BaseModel):
    name: str


class GroupCreated(GroupCreate):
    id: int


Group = GroupCreated


class GroupCreateWithScopes(BaseModel):
    name: str
    scope_ids: List[ScopeEnum]


class GroupCreatedWithScopes(GroupCreateWithScopes):
    id: int


GroupWithScopes = (
    GroupUpdateWithScopes
) = GroupUpdatedWithScopes = GroupCreatedWithScopes
