from back.db.table import UserElasticCountQueryBase, UserElasticSearchQueryBase
from tests.general.database import datetime_validator


def test_elasticsearch_query_validator():
    assert datetime_validator(UserElasticCountQueryBase, "validate_created")
    assert datetime_validator(UserElasticCountQueryBase, "validate_modified")
    assert datetime_validator(UserElasticSearchQueryBase, "validate_created")
    assert datetime_validator(UserElasticSearchQueryBase, "validate_modified")
