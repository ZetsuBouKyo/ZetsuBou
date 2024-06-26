import json
from typing import Union

import pytest

from back.db.crud import CrudUserElasticCountQuery, CrudUserElasticSearchQuery
from back.db.model import (
    UserElasticCountQueryCreate,
    UserElasticCountQueryUpdate,
    UserElasticSearchQueryCreate,
    UserElasticSearchQueryUpdate,
)
from tests.general.session import UserSession


async def case_1(
    crud: Union[CrudUserElasticCountQuery, CrudUserElasticSearchQuery],
    create_model: Union[UserElasticCountQueryCreate, UserElasticSearchQueryCreate],
    update_model: Union[UserElasticCountQueryUpdate, UserElasticSearchQueryUpdate],
):
    async with UserSession() as session:
        user = session.created_user_with_groups
        count_by_user_id_0 = await crud.count_by_user_id(user.id)

        query_name_1 = "test_1"
        query_json_1 = {"body": {"query": {"match_all": {}}}}
        query_1 = create_model(user_id=user.id, name=query_name_1, query=query_json_1)
        query_1_created = await crud.create(query_1)

        count_by_user_id_1 = await crud.count_by_user_id(user.id)

        assert count_by_user_id_1 == count_by_user_id_0 + 1

        assert query_1.name == query_1_created.name
        assert query_json_1 == json.loads(query_1_created.query)

        query_1_from_db = await crud.get_row_by_id_and_user_id(
            query_1_created.id, user.id
        )
        assert query_1.name == query_1_from_db.name
        assert query_json_1 == json.loads(query_1_from_db.query)

        queries = await crud.get_rows_by_user_id_order_by_id(user.id)
        assert len(queries) == 1

        query_name_2 = "test_2"
        query_2 = update_model(
            id=query_1_created.id,
            user_id=user.id,
            name=query_name_2,
            query=query_json_1,
        )
        await crud.update_by_id(query_2)
        query_2_updated = await crud.get_row_by_id(query_1_created.id)
        assert query_2_updated.name == query_name_2

        query_name_3 = "test_3"
        query_json_3 = {"body": {"query": {"match_all": {}}}}
        query_3 = create_model(user_id=user.id, name=query_name_3, query=query_json_3)
        query_3_created = await crud.create(query_3)
        await crud.delete_by_id_and_user_id(query_3_created.id, user.id)
        query_3_deleted = await crud.get_row_by_id(query_3_created.id)
        assert query_3_deleted is None

        with pytest.raises(Exception):
            query_name_4 = "test_4"
            query_json_4 = ""
            create_model(user_id=user.id, name=query_name_4, query=query_json_4)

    queries = await crud.get_rows_by_user_id_order_by_id(user.id)
    assert len(queries) == 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_crud_elasticsearch_count_query():
    await case_1(
        CrudUserElasticCountQuery,
        UserElasticCountQueryCreate,
        UserElasticCountQueryUpdate,
    )


@pytest.mark.asyncio
@pytest.mark.integration
async def test_crud_elasticsearch_search_query():
    await case_1(
        CrudUserElasticSearchQuery,
        UserElasticSearchQueryCreate,
        UserElasticSearchQueryUpdate,
    )
