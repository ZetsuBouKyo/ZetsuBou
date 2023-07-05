from typing import Union

from fastapi import HTTPException

from back.db.model import (
    UserElasticCountQueryCreate,
    UserElasticCountQueryUpdate,
    UserElasticSearchQueryCreate,
    UserElasticSearchQueryUpdate,
)


def verify_user_id(
    user_id: int,
    query: Union[
        UserElasticCountQueryCreate,
        UserElasticCountQueryUpdate,
        UserElasticSearchQueryCreate,
        UserElasticSearchQueryUpdate,
    ],
):
    if query.user_id is None:
        query.user_id = user_id
    elif user_id != query.user_id:
        raise HTTPException(
            status_code=409, detail="Conflict between user_id and query.user_id"
        )
