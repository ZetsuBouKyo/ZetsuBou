from back.db.crud import (
    CrudGroup,
    CrudScope,
    CrudUser,
    CrudUserGroup,
    CrudUserQuestCategory,
)
from back.db.model import (
    GroupCreate,
    UserQuestCategoryCreate,
    UserQuestCategoryEnum,
    UserWithGroupsCreate,
)
from back.db.table import Base
from back.model.group import BuiltInGroupEnum
from back.session.async_db import async_session
from back.settings import setting

ADMIN_GROUP_NAME = BuiltInGroupEnum.admin.value
ADMIN_NAME = setting.app_admin_name
ADMIN_EMAIL = setting.app_admin_email
ADMIN_PASSWORD = setting.app_admin_password

DATABASE_INIT = setting.database_initialization

ELASTIC_COUNT_QUEST = UserQuestCategoryEnum.ELASTIC_COUNT_QUEST.value


async def _init_table_data():
    # create scopes
    await CrudScope.init()

    # create groups
    await CrudGroup.init()

    # create admin group
    admin_group_name = ADMIN_GROUP_NAME
    admin_group = await CrudGroup.get_row_by_name(admin_group_name)
    if admin_group is None:
        admin_group = await CrudGroup.create(GroupCreate(name=admin_group_name))

    # create admin
    admin_name = ADMIN_NAME
    admin_email = ADMIN_EMAIL
    admin_password = ADMIN_PASSWORD
    admin_user = await CrudUser.get_row_by_email(admin_email)
    if admin_name and admin_email and admin_password:
        admin_user_groups = await CrudUserGroup.get_rows_by_group_id_order_by_id(
            admin_group.id
        )
        if len(admin_user_groups) == 0:
            if admin_user is None:
                admin_user = await CrudUser.create_with_groups(
                    UserWithGroupsCreate(
                        name=admin_name,
                        email=admin_email,
                        password=admin_password,
                        group_ids=[admin_group.id],
                    )
                )

    # create quest
    elastic_count_quest = ELASTIC_COUNT_QUEST
    user_quest_elastic_count_category = await CrudUserQuestCategory.get_row_by_name(
        elastic_count_quest
    )
    if user_quest_elastic_count_category is None:
        await CrudUserQuestCategory.create(
            UserQuestCategoryCreate(**{"name": elastic_count_quest})
        )


async def create_tables():
    async with async_session.async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_table():
    await create_tables()
    if DATABASE_INIT:
        await _init_table_data()
