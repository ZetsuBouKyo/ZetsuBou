from typing import List

import pytest
from faker import Faker

from back.db.crud import CrudUser
from back.db.model import UserWithGroupsCreate
from tests.general.logger import logger
from tests.general.session.db.base import SQLiteSession


class UserSession(SQLiteSession):
    def __init__(
        self,
        name: str = None,
        email: str = None,
        password: str = None,
        group_ids: List[int] = [],
    ):
        fake = Faker()
        self.name = name
        self.email = email
        self.password = password
        self.group_ids = group_ids

        if self.name is None:
            self.name = fake.name()
        if self.email is None:
            self.email = fake.email()
        if self.password is None:
            self.password = fake.password()

    async def enter(self):
        self.user_with_groups = UserWithGroupsCreate(
            name=self.name,
            email=self.email,
            password=self.password,
            group_ids=self.group_ids,
        )
        self.created_user_with_groups = await CrudUser.create_with_groups(
            self.user_with_groups
        )

        logger.info(f"user ID: {self.created_user_with_groups.id}")
        logger.info(f"user name: {self.name}")
        logger.info(f"user email: {self.email}")
        logger.info(f"user group ids: {self.group_ids}")
        logger.info(f"user password: {self.password}")

    async def exit(self):
        await CrudUser.delete_by_id(self.created_user_with_groups.id)


@pytest.mark.asyncio
async def test():  # pragma: no cover
    async with UserSession() as session:
        u = session.created_user_with_groups

    deleted_user = await CrudUser.get_row_by_id(u.id)
    assert deleted_user is None
