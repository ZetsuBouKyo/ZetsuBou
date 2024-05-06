from pydantic import BaseModel

from back.model.string import TagStr


class TagAttributeCreate(BaseModel):
    name: TagStr


class TagAttributeCreated(TagAttributeCreate):
    id: int


TagAttribute = TagAttributeUpdate = TagAttributeCreated
