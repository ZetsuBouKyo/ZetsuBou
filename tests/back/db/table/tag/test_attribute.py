from back.db.table import TagAttributeBase


def test_tag_attribute():
    tag_attribute_id = 1
    tag_attribute_name = "Admin"
    tag_attribute = TagAttributeBase(id=tag_attribute_id, name=tag_attribute_name)
    assert tag_attribute.name == tag_attribute_name.lower()
