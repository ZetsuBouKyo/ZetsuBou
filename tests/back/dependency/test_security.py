from datetime import timedelta

import pytest
from fastapi import HTTPException
from fastapi.security import SecurityScopes

from back.dependency.security import (
    api_security,
    do_nothing,
    extract_token,
    extract_token_from_cookies,
    verify_api_with_scopes,
    verify_view_with_scope,
    verify_with_scopes,
    view_security,
)
from back.model.group import BuiltInGroupEnum
from back.model.scope import ScopeEnum
from back.security import Token, create_access_token
from back.utils.exceptions import NotAuthenticatedException, RequiresLoginException
from lib.faker import ZetsuBouFaker
from tests.general.logger import logger
from tests.general.summary import print_divider


def test_extract_token():
    assert extract_token(None) is None

    sub_1 = 1
    groups_1 = [BuiltInGroupEnum.admin.value]
    token_1 = create_access_token(sub_1, groups=groups_1)
    extracted_token_1 = extract_token(token_1)
    logger.info(f"sub: {sub_1}")
    logger.info(f"groups: {groups_1}")
    logger.info(f"token: {token_1}")
    logger.info(f"extracted token: {extracted_token_1}")
    assert extracted_token_1.sub == sub_1
    assert extracted_token_1.groups == groups_1
    print_divider()

    faker = ZetsuBouFaker()
    token_2 = faker.random_string(64)
    logger.info(f"token: {token_2}")
    with pytest.raises(HTTPException):
        extract_token(token_2)
    print_divider()

    sub_3 = 1
    groups_3 = [BuiltInGroupEnum.admin.value]
    expires_delta_3 = timedelta(minutes=-200)
    token_3 = create_access_token(sub_3, groups=groups_3, expires_delta=expires_delta_3)
    logger.info(f"sub: {sub_3}")
    logger.info(f"groups: {groups_3}")
    logger.info(f"token: {token_3}")
    with pytest.raises(HTTPException):
        extract_token(token_3)


def test_extract_token_from_cookies():
    assert extract_token_from_cookies(None) is None

    sub_1 = 1
    groups_1 = [BuiltInGroupEnum.admin.value]
    token_1 = create_access_token(sub_1, groups=groups_1)
    extracted_token_1 = extract_token_from_cookies(token_1)
    logger.info(f"sub: {sub_1}")
    logger.info(f"groups: {groups_1}")
    logger.info(f"token: {token_1}")
    logger.info(f"extracted token: {extracted_token_1}")
    print_divider()

    faker = ZetsuBouFaker()
    token_2 = faker.random_string(64)
    logger.info(f"token: {token_2}")
    assert extract_token_from_cookies(token_2) is None
    print_divider()

    sub_3 = 1
    groups_3 = [BuiltInGroupEnum.admin.value]
    expires_delta_3 = timedelta(minutes=-200)
    token_3 = create_access_token(sub_3, groups=groups_3, expires_delta=expires_delta_3)
    logger.info(f"sub: {sub_3}")
    logger.info(f"groups: {groups_3}")
    logger.info(f"token: {token_3}")
    assert extract_token_from_cookies(token_3) is None


@pytest.mark.asyncio(scope="session")
async def test_verify_with_scopes():
    security_scopes_1 = SecurityScopes()
    with pytest.raises(NotAuthenticatedException):
        logger.info(f"scopes: {security_scopes_1.scopes}")
        await verify_with_scopes(security_scopes_1, None)
    print_divider()

    sub_2 = 1
    scopes_2 = [
        ScopeEnum.elasticsearch_analyzers_get.value,
        ScopeEnum.elasticsearch_query_examples_get.value,
    ]
    security_scopes_2 = SecurityScopes(scopes=scopes_2)
    token_2 = Token(sub=sub_2, exp=200, scopes=scopes_2)
    logger.info(f"route scopes: {scopes_2}")
    logger.info(f"token: {token_2}")
    res_2 = await verify_with_scopes(security_scopes_2, token_2)
    assert res_2 is True
    print_divider()

    # test the admin group
    sub_3 = 1
    scopes_3 = [
        ScopeEnum.elasticsearch_analyzers_get.value,
        ScopeEnum.elasticsearch_query_examples_get.value,
    ]
    security_scopes_3 = SecurityScopes(scopes=scopes_3)
    groups_3 = [BuiltInGroupEnum.admin.value]
    token_3 = Token(sub=sub_3, exp=200, groups=groups_3)
    logger.info(f"route scopes: {scopes_3}")
    logger.info(f"token: {token_3}")
    res_3 = await verify_with_scopes(security_scopes_3, token_3)
    assert res_3 is True
    print_divider()

    # test the guest group
    sub_4 = 1
    scopes_4 = [ScopeEnum.tag_post.value]
    groups_4 = [BuiltInGroupEnum.guest.value]
    security_scopes_4 = SecurityScopes(scopes=scopes_4)
    token_4 = Token(sub=sub_4, exp=200, groups=groups_4)
    with pytest.raises(NotAuthenticatedException):
        logger.info(f"route scopes: {scopes_4}")
        logger.info(f"token: {token_4}")
        await verify_with_scopes(security_scopes_4, token_4)

    faker = ZetsuBouFaker()
    sub_5 = 1
    scopes_5 = [ScopeEnum.tag_post.value]
    groups_5 = [faker.random_string()]
    security_scopes_5 = SecurityScopes(scopes=scopes_5)
    token_5 = Token(sub=sub_5, exp=200, groups=groups_5)
    with pytest.raises(NotAuthenticatedException):
        logger.info(f"route scopes: {scopes_5}")
        logger.info(f"token: {token_5}")
        await verify_with_scopes(security_scopes_5, token_5)


@pytest.mark.asyncio(scope="session")
async def test_verify_api_with_scopes():
    sub_1 = 1
    scopes_1 = [
        ScopeEnum.elasticsearch_analyzers_get.value,
        ScopeEnum.elasticsearch_query_examples_get.value,
    ]
    security_scopes_1 = SecurityScopes(scopes=scopes_1)
    token_1 = Token(sub=sub_1, exp=200, scopes=scopes_1)
    logger.info(f"route scopes: {scopes_1}")
    logger.info(f"token: {token_1}")
    await verify_api_with_scopes(security_scopes_1, token_1)


@pytest.mark.asyncio(scope="session")
async def test_verify_view_with_scope():
    security_scopes_1 = SecurityScopes()
    with pytest.raises(RequiresLoginException):
        logger.info(f"scopes: {security_scopes_1.scopes}")
        await verify_view_with_scope(security_scopes_1, None)


def test_api_and_view_security():
    api_security()
    api_security(app_security=False)
    view_security()
    view_security(app_security=False)


@pytest.mark.asyncio(scope="session")
async def test_do_nothing():
    await do_nothing()
