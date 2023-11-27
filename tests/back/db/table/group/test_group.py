from back.db.table import GroupBase


def test_group():
    group_id = 1
    group_name = "Admin"
    group = GroupBase(id=group_id, name=group_name)
    assert group.name == group_name.lower()
