from pydantic import BaseModel


class TagCategoryCreate(BaseModel):
    linked_id: int
    token_id: int


class TagCategoryCreated(TagCategoryCreate):
    id: int


TagCategory = TagCategoryUpdate = TagCategoryCreated
