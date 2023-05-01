from pydantic import BaseModel


class TagAttributeCreate(BaseModel):
    name: str


class TagAttributeCreated(BaseModel):
    id: int
    name: str


class TagAttributeUpdate(BaseModel):
    id: int
    name: str


class TagAttribute(BaseModel):
    id: int
    name: str
