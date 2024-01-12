from back.db.table import UserElasticCountQuestBase, UserQuestBase
from tests.general.database import datetime_validator


def test_user_quest_validator():
    assert datetime_validator(UserElasticCountQuestBase, "validate_created")
    assert datetime_validator(UserElasticCountQuestBase, "validate_modified")
    assert datetime_validator(UserQuestBase, "validate_created")
    assert datetime_validator(UserQuestBase, "validate_modified")
