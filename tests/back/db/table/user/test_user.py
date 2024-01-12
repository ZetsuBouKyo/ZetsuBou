from back.db.table import UserBase
from tests.general.database import datetime_validator


def test_user_validator():
    assert datetime_validator(UserBase, "validate_created")
    assert datetime_validator(UserBase, "validate_last_signin")
