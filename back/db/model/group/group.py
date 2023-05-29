from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str


class GroupCreated(GroupCreate):
    id: int


Group = GroupUpdate = GroupUpdated = GroupCreated
