import copy
from collections import deque
from typing import Dict, List

from elasticsearch import AsyncElasticsearch

from back.model.elasticsearch import AnalyzerEnum, ElasticsearchField
from back.session.async_elasticsearch import get_async_elasticsearch
from back.settings import setting

indices = [
    setting.model_dump()[key]
    for key in setting.model_dump().keys()
    if key.startswith("elastic_index")
]

settings = {
    "analysis": {
        "analyzer": {
            AnalyzerEnum.DEFAULT.value: {
                "tokenizer": "zetsubou_default_tokenizer",
                "filter": [
                    "lowercase",
                    "unique",
                    "zetsubou_default_length",
                ],
            },
            AnalyzerEnum.SYNONYM.value: {
                "tokenizer": "zetsubou_default_tokenizer",
                "filter": [
                    "lowercase",
                    "unique",
                    "zetsubou_default_length",
                    "zetsubou_synonym",
                ],
            },
            AnalyzerEnum.STANDARD.value: {"type": "standard"},
            AnalyzerEnum.NGRAM.value: {
                "tokenizer": "zetsubou_ngram_tokenizer",
                "filter": ["lowercase", "unique", "zetsubou_default_length"],
            },
            AnalyzerEnum.URL.value: {
                "tokenizer": "zetsubou_url_tokenizer",
                "filter": ["lowercase", "unique", "zetsubou_default_length"],
            },
        },
        "tokenizer": {
            "zetsubou_default_tokenizer": {
                "type": "pattern",
                # Special Regex Characters: ., +, *, ?, ^, $, (, ), [, ], {, }, |, \
                "pattern": r"[ \(\)\{\}｛｝\[\]【】〔〕〖〗《》<>⟨⟩「」『』\|｜_\-\+~～：“”‘’'`\"；!！\?？\.,，/、\\\\。\^@#$%&=]",  # noqa
            },
            "zetsubou_ngram_tokenizer": {
                "type": "ngram",
                "min_gram": 1,
                "max_gram": 1,
            },
            "zetsubou_url_tokenizer": {
                "type": "pattern",
                "pattern": "(://)|(/)",
            },
        },
        "filter": {
            "zetsubou_default_length": {"type": "length", "min": 1},
            "zetsubou_synonym": {
                "type": "synonym_graph",
                "synonyms_path": "analysis/synonym.txt",
                "updateable": True,
            },
        },
    }
}

name_fields = {
    "keyword": {"type": "keyword", "ignore_above": 256},
    "default": {
        "type": "text",
        "analyzer": AnalyzerEnum.DEFAULT.value,
        "search_analyzer": AnalyzerEnum.SYNONYM.value,
    },
    "standard": {
        "type": "text",
        "analyzer": AnalyzerEnum.STANDARD.value,
    },
    "ngram": {
        "type": "text",
        "analyzer": AnalyzerEnum.NGRAM.value,
    },
}

url_fields = {
    "keyword": {"type": "keyword", "ignore_above": 256},
    "standard": {
        "type": "text",
        "analyzer": AnalyzerEnum.STANDARD.value,
    },
    "ngram": {
        "type": "text",
        "analyzer": AnalyzerEnum.NGRAM.value,
    },
    "url": {
        "type": "text",
        "analyzer": AnalyzerEnum.URL.value,
    },
}

mappings = {
    "properties": {
        "path": {
            "type": "text",
            "fields": url_fields,
        },
        "name": {
            "type": "text",
            "fields": name_fields,
        },
        "raw_name": {
            "type": "text",
            "fields": name_fields,
        },
        "other_names": {
            "type": "text",
            "fields": name_fields,
        },
        "src": {
            "type": "text",
            "fields": url_fields,
        },
        "attributes": {"properties": {}},
    }
}

gallery_mappings = copy.deepcopy(mappings)
video_mappings = copy.deepcopy(mappings)


def get_field_analyzer_from_mapping(
    mapping: dict,
) -> Dict[ElasticsearchField, List[AnalyzerEnum]]:
    field_analyzer = {}
    field_name = ""
    stack = deque([(mapping, field_name)])
    while stack:
        _mapping, field_base_name = stack.popleft()
        are_properties = _mapping.get("properties", None)
        if are_properties is not None:
            for field_name, field_properties in _mapping["properties"].items():
                if field_base_name == "":
                    next_field_name = field_name
                else:
                    next_field_name = f"{field_base_name}.{field_name}"
                stack.append((field_properties, next_field_name))
        else:
            _fields = _mapping.get("fields", None)
            if _fields is None:
                continue
            field_analyzer[field_base_name] = list(_fields.keys())
    return field_analyzer


async def safe_create(session: AsyncElasticsearch, index: str, body: dict):
    if not await session.indices.exists(index=index):
        await session.indices.create(index=index, body=body)


async def create_gallery(session: AsyncElasticsearch, index: str):
    body = {
        "settings": settings,
        "mappings": gallery_mappings,
    }
    await safe_create(session, index, body)


async def create_video(session: AsyncElasticsearch, index: str):
    body = {
        "settings": settings,
        "mappings": video_mappings,
    }
    await safe_create(session, index, body)


async def create_tag(session: AsyncElasticsearch, index):
    body = {"settings": settings}
    await safe_create(session, index, body)


async def init_indices(session: AsyncElasticsearch = get_async_elasticsearch()):
    if not await session.ping():
        print("Elasticsearch not found")
        return

    await create_gallery(session, setting.elastic_index_gallery)
    await create_video(session, setting.elastic_index_video)
    await create_tag(session, setting.elastic_index_tag)
