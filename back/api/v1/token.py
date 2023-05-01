from datetime import timedelta

from back.db.crud import CrudUser
from back.security import create_access_token
from back.settings import setting
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

expired_in_minutes = setting.app_security_expired

router = APIRouter()


@router.post("")
async def get_token(form: OAuth2PasswordRequestForm = Depends()):
    user = await CrudUser.verify(form.username, form.password)

    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    expires_delta = timedelta(minutes=expired_in_minutes)

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
