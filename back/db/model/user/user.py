from typing import Optional

from pydantic import BaseModel, EmailStr

from back.utils.model import DatetimeStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreated(BaseModel):
    id: int
    name: str
    email: EmailStr


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
