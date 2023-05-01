from pydantic import BaseModel


class TagRepresentative(BaseModel):
    id: int
    linked_id: int
    token_id: int
