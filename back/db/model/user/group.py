from pydantic import BaseModel


class UserGroupCreate(BaseModel):
    user_id: int
    group_id: int


class UserGroup(BaseModel):
    id: int
    user_id: int
    group_id: int
