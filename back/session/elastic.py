from back.model.elastic import AnalyzerEnum
from back.settings import setting
from elasticsearch import Elasticsearch

hosts = setting.elastic_hosts
elastic_client = Elasticsearch(hosts=hosts)

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
        },
        "tokenizer": {
            "zetsubou_default_tokenizer": {
                "type": "pattern",
                "pattern": "[ (){}｛｝\\[\\]【】〔〕〖〗《》<>⟨⟩「」『』|｜_-~～：“”‘’'`\"；!！?？.,,，、。]",
            },
            "zetsubou_ngram_tokenizer": {
                "type": "ngram",
                "min_gram": 1,
                "max_gram": 1,
            },
        },
        "filter": {"zetsubou_default_length": {"type": "length", "min": 1}},
    }
}


def safe_create(client: Elasticsearch, index: str, body: dict):
    if not client.indices.exists(index=index):
        client.indices.create(index=index, body=body, ignore=400)


def create_gallery():
    body = {
        "settings": settings,
        "mappings": {
            "properties": {
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
                            },
                        },
                    }
                }
            }
        },
    }
    safe_create(elastic_client, setting.elastic_index_gallery, body)


def create_video():
    body = {
        "settings": settings,
        "mappings": {
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
                "attributes": {
                    "properties": {
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
                            },
                        },
                    }
                },
            }
        },
    }
    safe_create(elastic_client, setting.elastic_index_video, body)


def create_tag():
    body = {"settings": settings}
    safe_create(elastic_client, setting.elastic_index_tag, body)


def init_index():
    if not elastic_client.ping():
        return

    create_gallery()
    create_video()
    create_tag()
