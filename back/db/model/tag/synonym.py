from pydantic import BaseModel


class TagSynonymCreate(BaseModel):
    linked_id: int
    token_id: int


class TagSynonymCreated(BaseModel):
    id: int
    linked_id: int
    token_id: int


class TagSynonymUpdate(BaseModel):
    id: int
    linked_id: int
    token_id: int


class TagSynonym(BaseModel):
    id: int
    linked_id: int
    token_id: int
