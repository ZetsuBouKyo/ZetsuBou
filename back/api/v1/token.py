from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.param_functions import Form
from fastapi.security import OAuth2PasswordRequestForm

from back.db.crud import CrudUser
from back.security import create_access_token
from back.settings import setting

EXPIRED_IN_MINUTES = setting.app_security_expired

router = APIRouter(tags=["Token"])


class ZetsuBouOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default=None, pattern="password"),
        username: str = Form(),
        password: str = Form(),
        scope: str = Form(default=""),
        client_id: Optional[str] = Form(default=None),
        client_secret: Optional[str] = Form(default=None),
        expires: int = Form(default=None),
    ):
        self.grant_type = grant_type
        self.username = username
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
        self.expires = expires


@router.post("/token")
async def get_token(form: ZetsuBouOAuth2PasswordRequestForm = Depends()):
    user = await CrudUser.verify(form.username, form.password)

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if form.expires is None:
        expires_delta = timedelta(minutes=EXPIRED_IN_MINUTES)
    else:
        expires_delta = timedelta(minutes=form.expires)

    if not form.scopes:
        groups = await CrudUser.get_groups_by_id(user.id)
        scopes = [group.name for group in groups]
    else:
        # TODO:
        scopes = []

    return {
        "access_token": create_access_token(
            user.id, scopes=scopes, expires_delta=expires_delta
        ),
        "token_type": "bearer",
    }
