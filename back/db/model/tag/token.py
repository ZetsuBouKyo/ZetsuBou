from pydantic import BaseModel


class TagTokenCreate(BaseModel):
    name: str


class TagTokenCreated(TagTokenCreate):
    id: int


TagToken = TagTokenUpdate = TagTokenCreated
