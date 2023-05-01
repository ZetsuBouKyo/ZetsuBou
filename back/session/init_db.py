from back.db.crud import CrudGroup, CrudUser, CrudUserGroup, CrudUserQuestCategory
from back.db.model import (
    GroupCreate,
    ScopeEnum,
    UserCreate,
    UserGroupCreate,
    UserQuestCategoryCreate,
    UserQuestCategoryEnum,
)
from back.db.table import Base
from back.session.async_db import async_engine
from back.settings import setting


async def _init_table_data():
    group_name = ScopeEnum.admin.name
    admin_group = await CrudGroup.get_row_by_name(group_name)
    if admin_group is None:
        admin_group = await CrudGroup.create(GroupCreate(name=group_name))

    admin_name = setting.app_admin_name
    admin_email = setting.app_admin_email
    admin_password = setting.app_admin_password
    if admin_name and admin_email and admin_password:
        admin_user = await CrudUser.get_row_by_email(admin_email)
        if admin_user is None:
            admin_user = await CrudUser.create(
                UserCreate(name=admin_name, email=admin_email, password=admin_password)
            )
            await CrudUserGroup.create(
                UserGroupCreate(user_id=admin_user.id, group_id=admin_group.id)
            )

    ELASTIC_COUNT_QUEST = UserQuestCategoryEnum.ELASTIC_COUNT_QUEST.value
    user_quest_elastic_count_category = await CrudUserQuestCategory.get_row_by_name(
        ELASTIC_COUNT_QUEST
    )
    if user_quest_elastic_count_category is None:
        await CrudUserQuestCategory.create(
            UserQuestCategoryCreate(**{"name": ELASTIC_COUNT_QUEST})
        )


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def init_table():
    await create_tables()
    await _init_table_data()
