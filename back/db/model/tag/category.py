from pydantic import BaseModel


class TagCategoryCreate(BaseModel):
    linked_id: int
    token_id: int


class TagCategoryCreated(BaseModel):
    id: int
    linked_id: int
    token_id: int


TagCategory = TagCategoryCreated
