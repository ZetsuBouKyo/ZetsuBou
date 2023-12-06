from logging import Logger
from typing import List, Optional, Union

import pytest
from faker import Faker
from fastapi import HTTPException

from back.db.crud import CrudSettingFrontGallery, CrudSettingFrontVideo, CrudTagToken
from back.db.model import (
    SettingFrontGalleryUpdate,
    SettingFrontVideoUpdate,
    TagTokenCreate,
)
from back.model.tag import TagToken
from tests.general.db import SQLiteSession
from tests.general.summary import divider


class TagSession(SQLiteSession):
    def __init__(self, token_names: List[str] = []):
        self.token_names = token_names
        self.tokens: List[TagToken] = []
        self.name_to_token = {}

    async def enter(self):
        for name in self.token_names:
            token = TagTokenCreate(name=name)
            token_created = await CrudTagToken.create(token)
            self.tokens.append(token_created)
            self.name_to_token[token_created.name] = token_created

    async def exit(self):
        for token in self.tokens:
            await CrudTagToken.delete_by_id(token.id)

    def get_token_by_name(self, name: str) -> Optional[TagToken]:
        return self.name_to_token.get(name, None)


async def case_1(
    logger: Logger,
    crud: Union[CrudSettingFrontGallery, CrudSettingFrontVideo],
    update_model: Union[SettingFrontGalleryUpdate, SettingFrontVideoUpdate],
):
    faker = Faker()
    token_name_1 = faker.name()
    token_name_2 = faker.name()
    token_name_3 = faker.name()
    token_name_4 = faker.name()
    token_names = [token_name_1, token_name_2, token_name_3, token_name_4]
    assert len(token_names) == len(set(token_names))

    async with TagSession(token_names=token_names) as session:
        for token in session.tokens:
            logger.info(f"ID: {token.id} name: {token.name}")

        token_1 = session.get_token_by_name(token_name_1)
        token_2 = session.get_token_by_name(token_name_2)
        token_3 = session.get_token_by_name(token_name_3)
        token_4 = session.get_token_by_name(token_name_4)

        # test `crud._token_exists(...)`
        async with session.async_session() as _session:
            await crud._token_exists(_session, token_4.id)
            with pytest.raises(HTTPException):
                await crud._token_exists(_session, token_4.id + 1)

        # create settings
        settings_category_ids_1 = [token_1.id, token_2.id]
        settings_tag_field_ids_1 = [token_3.id, token_4.id]
        settings_1 = update_model(
            category_ids=settings_category_ids_1,
            tag_field_ids=settings_tag_field_ids_1,
        )
        await crud.update(settings_1)

        # test
        settings_interpretation_1 = await crud.get_interpretation()
        settings_interpretation_category_ids_1 = [
            token.id for token in settings_interpretation_1.categories
        ]
        settings_interpretation_tag_field_ids_1 = [
            token.id for token in settings_interpretation_1.tag_fields
        ]
        assert set(settings_interpretation_category_ids_1) == set(
            settings_category_ids_1
        )
        assert set(settings_interpretation_tag_field_ids_1) == set(
            settings_tag_field_ids_1
        )

        tokens_startswith_category_1 = await crud.startswith_category(token_1.name)
        assert len(tokens_startswith_category_1) > 0

        tokens_startswith_tag_field_1 = await crud.startswith_tag_field(token_3.name)
        assert len(tokens_startswith_tag_field_1) > 0

        # update settings
        settings_category_ids_2 = [token_1.id]
        settings_tag_field_ids_2 = [token_3.id]
        settings_2 = update_model(
            category_ids=settings_category_ids_2,
            tag_field_ids=settings_tag_field_ids_2,
        )
        await crud.update(settings_2)

        settings_interpretation_2 = await crud.get_interpretation()
        settings_interpretation_category_ids_2 = [
            token.id for token in settings_interpretation_2.categories
        ]
        settings_interpretation_tag_field_ids_2 = [
            token.id for token in settings_interpretation_2.tag_fields
        ]
        assert token_2.id not in settings_interpretation_category_ids_2
        assert token_4.id not in settings_interpretation_tag_field_ids_2

        # update settings
        settings_category_ids_3 = [token_1.id, token_2.id]
        settings_tag_field_ids_3 = [token_3.id, token_4.id]
        settings_3 = update_model(
            category_ids=settings_category_ids_3,
            tag_field_ids=settings_tag_field_ids_3,
        )
        await crud.update(settings_3)

        settings_interpretation_3 = await crud.get_interpretation()
        settings_interpretation_category_ids_3 = [
            token.id for token in settings_interpretation_3.categories
        ]
        settings_interpretation_tag_field_ids_3 = [
            token.id for token in settings_interpretation_3.tag_fields
        ]
        assert token_2.id in settings_interpretation_category_ids_3
        assert token_4.id in settings_interpretation_tag_field_ids_3

        # reset
        await crud.reset()
        settings_interpretation_reset = await crud.get_interpretation()
        assert len(settings_interpretation_reset.categories) == 0
        assert len(settings_interpretation_reset.tag_fields) == 0


@pytest.mark.asyncio
async def test_crud_gallery(logger: Logger):
    await case_1(logger, CrudSettingFrontGallery, SettingFrontGalleryUpdate)
    divider()
    await case_1(logger, CrudSettingFrontVideo, SettingFrontVideoUpdate)
