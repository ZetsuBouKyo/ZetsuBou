from pydantic import BaseModel


class TagTokenCreate(BaseModel):
    name: str


class TagTokenCreated(BaseModel):
    id: int
    name: str


class TagTokenUpdate(BaseModel):
    id: int
    name: str


class TagToken(BaseModel):
    id: int
    name: str
