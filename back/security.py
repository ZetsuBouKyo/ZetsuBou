from datetime import datetime, timedelta
from typing import Any, List, Union

from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from back.settings import setting

expired = setting.app_security_expired
secret = setting.app_security_secret
algorithm = setting.app_security_algorithm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    sub: int
    exp: int


def create_access_token(
    subject: Union[str, Any], scopes: List[str] = [], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=expired)
    to_encode = {"exp": expire, "sub": str(subject), "scopes": scopes}
    encoded_jwt = jwt.encode(
        to_encode,
        secret,
        algorithm=algorithm,
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)
