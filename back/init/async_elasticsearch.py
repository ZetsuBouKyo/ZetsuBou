from back.model.elastic import AnalyzerEnum
from back.session.async_elasticsearch import async_elasticsearch
from back.settings import setting
from elasticsearch import AsyncElasticsearch

indices = [
    setting.dict()[key]
    for key in setting.dict().keys()
    if key.startswith("elastic_index")
]

settings = {
    "analysis": {
        "analyzer": {
            AnalyzerEnum.DEFAULT.value: {
                "tokenizer": "zetsubou_default_tokenizer",
                "filter": ["lowercase", "unique", "zetsubou_default_length"],
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
                "pattern": "[ \(\)\{\}｛｝\[\]【】〔〕〖〗《》<>⟨⟩「」『』\|｜_\-\+~～：“”‘’'`\"；!！\?？\.,，/、\\\\。\^@#$%&=]",  # noqa
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
        "filter": {"zetsubou_default_length": {"type": "length", "min": 1}},
    }
}

gallery_mappings = {
    "properties": {
        "path": {
            "type": "text",
            "fields": {
                "keyword": {"type": "keyword", "ignore_above": 256},
                "ngram": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.NGRAM.value,
                },
                "url": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.URL.value,
                },
            },
        },
        "attributes": {
            "properties": {
                "name": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword", "ignore_above": 256},
                        "default": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.DEFAULT.value,
                        },
                        "standard": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.STANDARD.value,
                        },
                        "ngram": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.NGRAM.value,
                        },
                    },
                },
                "raw_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword", "ignore_above": 256},
                        "default": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.DEFAULT.value,
                        },
                        "standard": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.STANDARD.value,
                        },
                        "ngram": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.NGRAM.value,
                        },
                    },
                },
                "src": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword", "ignore_above": 256},
                        "default": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.DEFAULT.value,
                        },
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
                    },
                },
            }
        },
    }
}

video_mappings = {
    "properties": {
        "name": {
            "type": "text",
            "fields": {
                "keyword": {"type": "keyword", "ignore_above": 256},
                "default": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.DEFAULT.value,
                },
                "standard": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.STANDARD.value,
                },
                "ngram": {"type": "text", "analyzer": AnalyzerEnum.NGRAM.value},
            },
        },
        "other_names": {
            "type": "text",
            "fields": {
                "keyword": {"type": "keyword", "ignore_above": 256},
                "default": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.DEFAULT.value,
                },
                "standard": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.STANDARD.value,
                },
                "ngram": {"type": "text", "analyzer": AnalyzerEnum.NGRAM.value},
            },
        },
        "path": {
            "type": "text",
            "fields": {
                "keyword": {"type": "keyword", "ignore_above": 256},
                "ngram": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.NGRAM.value,
                },
                "url": {
                    "type": "text",
                    "analyzer": AnalyzerEnum.URL.value,
                },
            },
        },
        "attributes": {
            "properties": {
                "src": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword", "ignore_above": 256},
                        "ngram": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.NGRAM.value,
                        },
                        "url": {
                            "type": "text",
                            "analyzer": AnalyzerEnum.URL.value,
                        },
                    },
                },
            }
        },
    }
}


async def safe_create(session: AsyncElasticsearch, index: str, body: dict):
    if not await session.indices.exists(index=index):
        await session.indices.create(index=index, body=body)


async def create_gallery(session: AsyncElasticsearch):
    body = {
        "settings": settings,
        "mappings": gallery_mappings,
    }
    await safe_create(session, setting.elastic_index_gallery, body)


async def create_video(session: AsyncElasticsearch):
    body = {
        "settings": settings,
        "mappings": video_mappings,
    }
    await safe_create(session, setting.elastic_index_video, body)


async def create_tag(session: AsyncElasticsearch):
    body = {"settings": settings}
    await safe_create(session, setting.elastic_index_tag, body)


async def init_indices(session: AsyncElasticsearch = async_elasticsearch):
    if not await session.ping():
        print("Elasticsearch not found")
        return

    await create_gallery(session)
    await create_video(session)
    await create_tag(session)
