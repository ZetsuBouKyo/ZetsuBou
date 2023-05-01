from pydantic import BaseModel


class TagDefinition(BaseModel):
    name: str
    definition: str
