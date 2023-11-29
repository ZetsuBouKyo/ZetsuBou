from pydantic import BaseModel


class TagSynonymCreate(BaseModel):
    linked_id: int
    token_id: int


class TagSynonymCreated(TagSynonymCreate):
    id: int


TagSynonym = TagSynonymUpdate = TagSynonymCreated
