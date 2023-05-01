import unittest

from back.model.tag import Tag, TagCreate


def test_crud_post(client):
    client.get()
