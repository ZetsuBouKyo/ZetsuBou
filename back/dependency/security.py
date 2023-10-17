from typing import List

from fastapi import Cookie, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from jose.jwt import JWTError
from pydantic import BaseModel, ValidationError

from back.db.crud import CrudGroup
from back.model.scope import ScopeEnum
from back.settings import setting
from back.utils.exceptions import RequiresLoginException

APP_SECURITY = setting.app_security
SECRET = setting.app_security_secret
ALGORITHM = setting.app_security_algorithm

_scopes = {scope.value: scope.value for scope in ScopeEnum}

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="api/v1/token",
    scopes=_scopes,
    auto_error=False,
)


class Token(BaseModel):
    sub: int
    exp: int
    groups: List[str] = []
    scopes: List[str] = []


def get_not_authenticated_exception(scopes: str, detail: str = None):
    authenticate_value = "Bearer"
    if scopes:
        authenticate_value = f"Bearer scope={scopes}"

    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": authenticate_value},
    )


def decode_token(token: str) -> Token:
    payload = jwt.decode(
        token,
        SECRET,
        algorithms=[ALGORITHM],
    )
    return Token(**payload)


def extract_token(token: str = Depends(reusable_oauth2)) -> Token:
    if token is None:
        return None
    try:
        token = decode_token(token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Signature has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


def extract_token_from_cookies(token: str = Cookie(None)) -> Token:
    if token is None:
        return None
    try:
        token = decode_token(token)
    except (JWTError, ExpiredSignatureError):
        return None
    return token


async def verify_with_scopes(security_scopes: SecurityScopes, token: Token):
    if token is None:
        raise get_not_authenticated_exception(
            security_scopes.scope_str, detail="No token"
        )

    token_scope_set = set(token.scopes)

    remaining_scopes = set()
    for scope in security_scopes.scopes:
        if scope not in token_scope_set:
            remaining_scopes.add(scope)

    if not remaining_scopes:
        return True

    group_names = token.groups

    group_scopes = set()
    for group_name in group_names:
        group = await CrudGroup.get_row_with_scopes_by_name(group_name)
        scope_names = group.scope_names
        if scope_names is None:
            continue
        group_scopes |= set(scope_names)

    if remaining_scopes <= group_scopes:
        return True

    raise get_not_authenticated_exception(
        security_scopes.scope_str, detail="Not enough permissions"
    )


async def verify_api_with_scopes(
    security_scopes: SecurityScopes, token: Token = Depends(extract_token)
):
    await verify_with_scopes(security_scopes, token)


async def verify_view_with_scope(
    security_scopes: SecurityScopes, token: Token = Depends(extract_token_from_cookies)
):
    try:
        await verify_with_scopes(security_scopes, token)
    except HTTPException:
        raise RequiresLoginException(status_code=status.HTTP_401_UNAUTHORIZED)


async def do_nothing():
    pass


def api_user_security():
    pass


def api_security(scopes: List[str] = []) -> Security:
    if APP_SECURITY:
        return Security(verify_api_with_scopes, scopes=scopes)
    return Security(do_nothing, scopes=scopes)


def view_security(scopes: List[str] = []) -> Security:
    if APP_SECURITY:
        return Security(verify_view_with_scope, scopes=scopes)
    return Security(do_nothing, scopes=scopes)
