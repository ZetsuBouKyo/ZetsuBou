from datetime import timedelta

from back.security import (
    create_access_token,
    decode_token,
    get_hashed_password,
    verify_password,
)


def test_create_access_token():
    sub_1 = 1
    expires_delta_1 = timedelta(minutes=30)
    token_1 = create_access_token(sub_1, expires_delta=expires_delta_1)
    decoded_token_1 = decode_token(token_1)
    assert decoded_token_1.sub == sub_1

    sub_2 = 2
    token_2 = create_access_token(sub_2)
    decoded_token_2 = decode_token(token_2)
    assert decoded_token_2.sub == sub_2


def test_password():
    password = "123456"
    hashed_password = get_hashed_password(password)
    assert verify_password(password, hashed_password)
