from pydantic import BaseModel


class UserGroupCreate(BaseModel):
    user_id: int
    group_id: int


class UserGroupCreated(UserGroupCreate):
    id: int


UserGroup = UserGroupCreated
