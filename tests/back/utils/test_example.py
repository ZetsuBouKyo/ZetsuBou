from back.utils import get_example
from lib.faker import ZetsuBouFaker


def test_get_example():
    faker = ZetsuBouFaker()
    base_id = 1
    base_name = faker.name()
    base_group_ids = [1]
    base = {"id": base_id, "name": base_name, "group_ids": base_group_ids}

    example_1 = get_example("id", base=base)
    assert len(example_1) == 1
    assert example_1.get("id", None) == base_id
    assert example_1.get("name", None) is None
    assert example_1.get("group_ids", None) is None

    example_2 = get_example("id", "name", base=base)
    assert len(example_2) == 2
    assert example_2.get("id", None) == base_id
    assert example_2.get("name", None) == base_name
    assert example_2.get("group_ids", None) is None

    example_3 = get_example("id", "name", "group_ids", base=base)
    assert len(example_3) == 3
    assert example_3.get("id", None) == base_id
    assert example_3.get("name", None) == base_name
    assert example_3.get("group_ids", None) == base_group_ids
