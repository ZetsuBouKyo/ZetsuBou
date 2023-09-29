from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

from back.utils.model import DatetimeStr

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
    email: EmailStr
    name: Optional[str] = None
    password: str
    new_password: Optional[str] = None


class User(BaseModel):
    id: int
    name: str
    email: str
    created: DatetimeStr
    last_signin: DatetimeStr


class UserWithGroupCreate(UserCreate):
    group_ids: List[int]


class UserWithGroupCreated(UserCreated):
    group_ids: List[int] = Field(..., examples=[[1]])


class UserWithGroupUpdate(UserUpdate):
    group_ids: List[int]


class UserWithGroupRow(User):
    group_id: Optional[int] = None
    group_name: Optional[str] = None


class UserWithGroupAndHashedPasswordRow(UserWithGroupRow):
    hashed_password: str


class UserWithGroup(User):
    group_ids: List[int] = []
    group_names: List[str] = []


class UserWithGroupAndHashedPassword(UserWithGroup):
    hashed_password: str
