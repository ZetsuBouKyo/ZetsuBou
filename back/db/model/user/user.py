from back.utils.model import DatetimeStr
from pydantic import BaseModel, EmailStr


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
    name: str = None
    password: str
    new_password: str = None


class User(BaseModel):
    id: int
    name: str
    email: str
    created: DatetimeStr
    last_signin: DatetimeStr
