from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from back.model.string import DatetimeStr

field_group_ids = Field(..., examples=[[1]])


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreated(BaseModel):
    id: int = Field(..., examples=[1])
    name: str = Field(..., examples=["ZetsuBouKyo"])
    email: EmailStr = Field(..., examples=["zetsuboukyo@example.com"])


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str
    new_password: Optional[str] = None


class User(UserCreated):
    created: DatetimeStr
    last_signin: DatetimeStr


class UserWithHashedPassword(User):
    hashed_password: str


class UserWithGroupsCreate(UserCreate):
    group_ids: List[int]


class UserWithGroupsCreated(UserCreated):
    group_ids: List[int] = Field(..., examples=[[1]])


class UserWithGroupsUpdate(UserUpdate):
    group_ids: List[int]


class UserWithGroupRow(User):
    group_id: Optional[int] = None
    group_name: Optional[str] = None


class UserWithGroupAndHashedPasswordRow(UserWithGroupRow):
    hashed_password: str


class UserWithGroups(User):
    group_ids: List[int] = []
    group_names: List[str] = []


class UserWithGroupAndHashedPassword(UserWithGroups):
    hashed_password: str
