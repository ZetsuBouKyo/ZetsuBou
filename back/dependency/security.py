from typing import List

from fastapi import Cookie, Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, OAuth2PasswordBearer, SecurityScopes
from jose.exceptions import ExpiredSignatureError
from jose.jwt import JWTError
from pydantic import ValidationError

from back.db.crud import CrudGroup
from back.model.scope import ScopeEnum
from back.security import Token, decode_token
from back.settings import setting
from back.utils.exceptions import NotAuthenticatedException, RequiresLoginException

APP_SECURITY = setting.app_security
SECRET = setting.app_security_secret
ALGORITHM = setting.app_security_algorithm
TOKEN_URL = "api/v1/token"

_scopes = {scope.value: scope.value for scope in ScopeEnum}
http_bearer_description = (
    f"You can get the JWT (JSON Web Token) token from `/{TOKEN_URL}`."
)
http_bearer = HTTPBearer(
    scheme_name="HTTP Header Bearer Token", description=http_bearer_description
)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=TOKEN_URL,
    scopes=_scopes,
    auto_error=False,
)


def extract_token(
    token: str = Depends(reusable_oauth2), _: str = Depends(http_bearer)
) -> Token:
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
        raise NotAuthenticatedException(security_scopes.scope_str, detail="No token")

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

    raise NotAuthenticatedException(
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
