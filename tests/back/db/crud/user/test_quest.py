import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from back.db.crud import (
    CrudUserElasticCountQuery,
    CrudUserElasticCountQuest,
    CrudUserQuest,
    CrudUserQuestCategory,
)
from back.db.model import (
    UserElasticCountQueryCreate,
    UserElasticCountQuestCreate,
    UserElasticCountQuestUpdate,
    UserQuestCategoryEnum,
    UserQuestCreate,
    UserQuestUpdate,
)
from tests.general.session import UserSession


@pytest.mark.asyncio
async def test_crud():
    async with UserSession() as session:
        user = session.created_user_with_groups

        # create Elasticsearch count query
        query_name_1 = "test 1"
        query_json_1 = {"body": {"query": {"match_all": {}}}}
        query_1 = UserElasticCountQueryCreate(
            user_id=user.id, name=query_name_1, query=query_json_1
        )
        query_1_created = await CrudUserElasticCountQuery.create(query_1)

        query_name_2 = "test 2"
        query_json_2 = {"body": {"query": {"match_all": {}}}}
        query_2 = UserElasticCountQueryCreate(
            user_id=user.id, name=query_name_2, query=query_json_2
        )
        query_2_created = await CrudUserElasticCountQuery.create(query_2)

        query_name_3 = "test 3"
        query_json_3 = {"body": {"query": {"match_all": {}}}}
        query_3 = UserElasticCountQueryCreate(
            user_id=user.id, name=query_name_3, query=query_json_3
        )
        query_3_created = await CrudUserElasticCountQuery.create(query_3)

        # create Elasticsearch count quest
        elasticsearch_count_quest_name_1 = "test 1"
        elasticsearch_count_quest_1 = UserElasticCountQuestCreate(
            name=elasticsearch_count_quest_name_1,
            user_id=user.id,
            numerator_id=query_1_created.id,
            denominator_id=query_1_created.id,
        )
        elasticsearch_count_quest_1_created = await CrudUserElasticCountQuest.create(
            elasticsearch_count_quest_1
        )

        elasticsearch_count_quest_name_2 = "test 2"
        elasticsearch_count_quest_2 = UserElasticCountQuestCreate(
            name=elasticsearch_count_quest_name_2,
            user_id=user.id,
            numerator_id=query_2_created.id,
            denominator_id=query_2_created.id,
        )
        elasticsearch_count_quest_2_created = await CrudUserElasticCountQuest.create(
            elasticsearch_count_quest_2
        )

        elasticsearch_count_quest_name_3 = "test 3"
        elasticsearch_count_quest_3 = UserElasticCountQuestCreate(
            name=elasticsearch_count_quest_name_3,
            user_id=user.id,
            numerator_id=query_3_created.id,
            denominator_id=query_3_created.id,
        )
        elasticsearch_count_quest_3_created = await CrudUserElasticCountQuest.create(
            elasticsearch_count_quest_3
        )

        # test Elasticsearch count quest
        elasticsearch_count_quest_total_1 = (
            await CrudUserElasticCountQuest.count_by_user_id(user.id)
        )
        assert elasticsearch_count_quest_total_1 == 3

        elasticsearch_count_quest_1_by_id = (
            await CrudUserElasticCountQuest.get_row_by_id(
                elasticsearch_count_quest_1_created.id
            )
        )
        assert elasticsearch_count_quest_1_by_id is not None

        elasticsearch_count_quest_1_by_user_id_and_quest_id = (
            await CrudUserElasticCountQuest.get_row_by_user_id_and_quest_id(
                user.id, elasticsearch_count_quest_1_created.id
            )
        )
        assert elasticsearch_count_quest_1_by_user_id_and_quest_id is not None

        # update Elasticsearch count quest
        elasticsearch_count_quest_name_2_to_update = "test 2 update"
        elasticsearch_count_quest_2_to_update = UserElasticCountQuestUpdate(
            id=elasticsearch_count_quest_2_created.id,
            name=elasticsearch_count_quest_name_2_to_update,
            user_id=user.id,
            numerator_id=query_2_created.id,
            denominator_id=query_2_created.id,
        )
        await CrudUserElasticCountQuest.update_by_id(
            elasticsearch_count_quest_2_to_update
        )
        elasticsearch_count_quest_2_updated = (
            await CrudUserElasticCountQuest.get_row_by_id(
                elasticsearch_count_quest_2_to_update.id
            )
        )

        # test Elasticsearch count quest
        assert (
            elasticsearch_count_quest_2_created.id
            == elasticsearch_count_quest_2_updated.id
        )
        assert (
            elasticsearch_count_quest_2_created.name == elasticsearch_count_quest_name_2
        )
        assert (
            elasticsearch_count_quest_2_created.name
            != elasticsearch_count_quest_2_updated.name
        )
        assert (
            elasticsearch_count_quest_2_updated.name
            == elasticsearch_count_quest_name_2_to_update
        )

        elasticsearch_count_quests = (
            await CrudUserElasticCountQuest.get_rows_by_user_id_order_by_id(user.id)
        )
        assert len(elasticsearch_count_quests) == 3

        # get Elasticsearch count quest category
        elasticsearch_count_quest_category_name = (
            UserQuestCategoryEnum.ELASTIC_COUNT_QUEST.value
        )
        elasticsearch_count_quest_category = (
            await CrudUserQuestCategory.get_row_by_name(
                elasticsearch_count_quest_category_name
            )
        )
        assert elasticsearch_count_quest_category is not None
        elasticsearch_count_quest_category_by_id = (
            await CrudUserQuestCategory.get_row_by_id(
                elasticsearch_count_quest_category.id
            )
        )
        assert elasticsearch_count_quest_category_by_id is not None
        elasticsearch_count_quest_categories = (
            await CrudUserQuestCategory.get_rows_order_by_id()
        )
        assert len(elasticsearch_count_quest_categories) == 1

        # create quest
        quest_name_1 = "Quest 1"
        quest_priority_1 = 0
        quest_1 = UserQuestCreate(
            user_id=user.id,
            name=quest_name_1,
            category_id=elasticsearch_count_quest_category.id,
            quest_id=elasticsearch_count_quest_1_created.id,
            priority=quest_priority_1,
        )
        quest_1_created = await CrudUserQuest.create(quest_1)

        quest_name_2 = "Quest 2"
        quest_priority_2 = 1
        quest_2 = UserQuestCreate(
            user_id=user.id,
            name=quest_name_2,
            category_id=elasticsearch_count_quest_category.id,
            quest_id=elasticsearch_count_quest_1_created.id,
            priority=quest_priority_2,
        )

        with pytest.raises(IntegrityError):
            await CrudUserQuest.create(quest_2)

        quest_name_3 = "Quest 3"
        quest_priority_3 = -1
        with pytest.raises(ValidationError):
            UserQuestCreate(
                user_id=user.id,
                name=quest_name_3,
                category_id=elasticsearch_count_quest_category.id,
                quest_id=elasticsearch_count_quest_1_created.id,
                priority=quest_priority_3,
            )

        quest_name_4 = "Quest 4"
        quest_priority_4 = 4
        quest_4 = UserQuestCreate(
            user_id=user.id,
            name=quest_name_4,
            category_id=elasticsearch_count_quest_category.id,
            quest_id=elasticsearch_count_quest_2_created.id,
            priority=quest_priority_4,
        )
        quest_4_created = await CrudUserQuest.create(quest_4)

        quest_top = await CrudUserQuest.get_top_priority(user.id)
        assert quest_top[0].id == quest_1_created.id

        quests = await CrudUserQuest.get_rows_by_user_id_order_by_id(user.id)
        assert len(quests) == 2
        quests_count = await CrudUserQuest.count_by_user_id(user.id)
        assert quests_count == 2

        quest_name_4_to_update = "Quest 4 to update"
        quest_4_to_update = UserQuestUpdate(
            id=quest_4_created.id,
            user_id=user.id,
            name=quest_name_4_to_update,
            category_id=elasticsearch_count_quest_category.id,
            quest_id=elasticsearch_count_quest_2_created.id,
            priority=quest_priority_4,
        )
        await CrudUserQuest.update_by_id(quest_4_to_update)
        quest_4_updated = await CrudUserQuest.get_row_by_id(quest_4_created.id)
        assert quest_4_updated.name == quest_name_4_to_update

        quest_name_5 = "Quest 5"
        quest_priority_5 = 5
        quest_5 = UserQuestCreate(
            user_id=user.id,
            name=quest_name_5,
            category_id=elasticsearch_count_quest_category.id,
            quest_id=elasticsearch_count_quest_3_created.id,
            priority=quest_priority_5,
        )
        quest_5_created = await CrudUserQuest.create(quest_5)
        await CrudUserQuest.delete_by_id_and_user_id(quest_5_created.id, user.id)
        quest_5_deleted = await CrudUserQuest.get_row_by_id(quest_5_created.id)
        assert quest_5_deleted is None

        await CrudUserElasticCountQuery.delete_by_id_and_user_id(
            query_2_created.id, user.id
        )
        query_2_deleted = await CrudUserElasticCountQuery.get_row_by_id(
            query_2_created.id
        )
        assert query_2_deleted is None
        elasticsearch_count_quest_2_deleted = (
            await CrudUserElasticCountQuest.get_row_by_id(
                elasticsearch_count_quest_2_created.id
            )
        )
        assert elasticsearch_count_quest_2_deleted is None

        await CrudUserElasticCountQuest.delete_by_id_and_user_id(
            elasticsearch_count_quest_3_created.id, user.id
        )
        elasticsearch_count_quest_3_deleted = (
            await CrudUserElasticCountQuest.get_row_by_id(
                elasticsearch_count_quest_3_created.id
            )
        )
        assert elasticsearch_count_quest_3_deleted is None

    elasticsearch_count_quests = (
        await CrudUserElasticCountQuest.get_rows_by_user_id_order_by_id(user.id)
    )
    assert len(elasticsearch_count_quests) == 0

    quests = await CrudUserQuest.get_rows_by_user_id_order_by_id(user.id)
    assert len(quests) == 0
