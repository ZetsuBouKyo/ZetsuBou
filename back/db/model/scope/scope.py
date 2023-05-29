from pydantic import BaseModel


class Scope(BaseModel):
    id: int
    name: str


ScopeCreated = ScopeUpdate = ScopeUpdated = Scope


class ScopeCreate(BaseModel):
    name: str
