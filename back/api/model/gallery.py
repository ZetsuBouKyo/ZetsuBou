from typing import List

from pydantic import BaseModel


class Attributes(BaseModel):
    category: List[str] = []


class CustomQuery(BaseModel):
    body: dict


query_examples = {
    "Exists": {
        "summary": "Exists",
        "description": (
            "You could change the <field-name> with field you want. "
            "For nested field, you could put the dot between parent and child. e.g. "
            "'attributes.rating'."
        ),
        "value": {
            "body": {
                "query": {
                    "exists": {"field": "<field-name>"},
                }
            }
        },
    },
    "Missing": {
        "summary": "Missing",
        "description": (
            "You could change the <field-name> with field you want. "
            "For nested field, you could put the dot between parent and child. e.g. "
            "'attributes.rating'."
        ),
        "value": {
            "body": {
                "query": {"bool": {"must_not": {"exists": {"field": "<field-name>"}}}}
            }
        },
    },
    "Range": {
        "summary": "Range",
        "description": "You could get the range of number, datetime, and so on.",
        "value": {
            "body": {
                "query": {
                    "range": {
                        "timestamp": {"gte": "<datetime:2022-01-06T13:30:05.976321>"}
                    }
                }
            }
        },
    },
    "Terms": {
        "summary": "Terms",
        "description": (
            "You could search the specific value under specific field. "
            "With '.keyword' suffixed to the field, you could search for the values "
            "which are exactly the same."
        ),
        "value": {"body": {"query": {"terms": {"<field>": ["<value>"]}}}},
    },
    "Match": {
        "summary": "Match",
        "description": "You could search the <value> under <field>.",
        "value": {"body": {"query": {"match": {"<field>": "<value>"}}}},
    },
    "MatchAll": {
        "summary": "MatchAll",
        "description": "Get all docs.",
        "value": {"body": {"query": {"match_all": {}}}},
    },
    "CountValuesOfField": {
        "summary": "CountValuesOfField",
        "description": "Count the values of specific field.",
        "value": {
            "body": {
                "aggs": {
                    "whatever_you_like_here": {
                        "terms": {"field": "<field>.keyword", "size": 10000}
                    }
                },
                "size": 0,
            }
        },
    },
}
