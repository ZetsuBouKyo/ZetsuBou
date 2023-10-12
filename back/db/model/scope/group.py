from pydantic import BaseModel


class ScopeGroup(BaseModel):
    id: int
    scope_id: int
    group_id: int
