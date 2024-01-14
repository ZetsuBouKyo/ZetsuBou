from back.model.group import BuiltInGroupEnum
from back.security import create_access_token


def get_admin_headers() -> dict:
    token = create_access_token("1", groups=[BuiltInGroupEnum.admin.value])
    bearer = f"Bearer {token}"
    return {"Authorization": bearer}


def get_admin_cookies():
    token = create_access_token("1", groups=[BuiltInGroupEnum.admin.value])
    return {"token": token}
