from pydantic import BaseModel


class ScopeCreate(BaseModel):
    name: str


class ScopeCreated(ScopeCreate):
    id: int


Scope = ScopeUpdate = ScopeUpdated = ScopeCreated
