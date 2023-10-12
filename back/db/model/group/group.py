from typing import List, Optional

from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupCreated(GroupCreate):
    id: int


Group = GroupUpdate = GroupUpdated = GroupCreated


class GroupWithScopeIdsSafeCreate(GroupCreate):
    scope_ids: List[int]


class GroupWithScopes(GroupWithScopeIdsSafeCreate):
    id: int
    scope_names: List[str]


class GroupWithScopeIdsUpdate(GroupWithScopeIdsSafeCreate):
    id: int


class GroupWithScopeRow(GroupCreated):
    scope_id: Optional[int] = None
    scope_name: Optional[str] = None
