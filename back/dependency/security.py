from typing import List

from back.db.crud import CrudGroup, CrudScope
from back.model.scope import ScopeEnum
from back.settings import setting
from back.utils.exceptions import RequiresLoginException
from fastapi import Cookie, Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt
from jose.exceptions import ExpiredSignatureError
from jose.jwt import JWTError
from pydantic import BaseModel, ValidationError

APP_SECURITY = setting.app_security
SECRET = setting.app_security_secret
ALGORITHM = setting.app_security_algorithm

_scopes = {
    "admin": "admin",
    "guest": "guest",
    ScopeEnum.elasticsearch_query_examples_get.name: "get elasticsearch query example",
}

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="api/v1/token",
    scopes=_scopes,
    auto_error=False,
)


class Scope:
    def __init__(self):
        self._id_to_name = {}
        self._name_to_id = {}
        for scope in ScopeEnum:
            self._id_to_name[scope.value] = scope.name
            self._name_to_id[scope.name] = scope.value

    def get_name_by_id(self, id: int) -> str:
        return self._id_to_name.get(id, None)

    def get_id_by_name(self, name: str) -> int:
        return self._name_to_id.get(name, None)


_scope = Scope()


class Token(BaseModel):
    sub: int
    exp: int
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
    if ScopeEnum.admin.name in token_scope_set:
        return True

    remaining_scopes = set()
    for scope in security_scopes.scopes:
        # token_scope_set should be in ScopeEnum or Group.name
        if scope not in token_scope_set:
            remaining_scopes.add(scope)

    if not remaining_scopes:
        return True

    # This part could be optimized by caching the group-to-scope table.
    group_scopes = set()
    for scope in token_scope_set:
        if _scope.get_id_by_name(scope) is not None:
            continue
        group = await CrudGroup.get_row_by_name(scope)
        if group is None:
            get_not_authenticated_exception(
                security_scopes.scope_str, detail=f"Scope: {scope} not found"
            )

        scopes_by_group_id = await CrudScope.get_all_rows_by_group_id_order_by_id(
            group.id
        )
        for s in scopes_by_group_id:
            group_scopes.add(_scope.get_name_by_id(s.id))

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
