from logging import Logger
from typing import Set

import pytest
from pydantic import BaseModel

from back.model.elasticsearch import AnalyzerEnum
from back.session.async_elasticsearch import get_async_elasticsearch
from back.settings import setting
from tests.general.session import ElasticsearchSession
from tests.general.summary import divider


class DataModel(BaseModel):
    index: str
    text: str
    analyzer: AnalyzerEnum
    answer: Set[str]


raw_data = [
    {
        "index": setting.elastic_index_gallery,
        "text": "[中文] 安安\你好/3 方程式^次方 ! (唐詩三百首) info@gmail.com $1000 %2 18樓-十九 [Chinese]",
        "analyzer": AnalyzerEnum.DEFAULT.value,
        "answer": {
            "1000",
            "18樓",
            "2",
            "3",
            "chinese",
            "com",
            "gmail",
            "info",
            "中文",
            "你好",
            "十九",
            "唐詩三百首",
            "安安",
            "方程式",
            "次方",
        },
    },
    {
        "index": setting.elastic_index_gallery,
        "text": "[中文] 安安\你好/3 方程式^次方 ! (唐詩三百首) info@gmail.com $1000 %2 18樓-十九 [Chinese]",
        "analyzer": AnalyzerEnum.KEYWORD.value,
        "answer": {
            "[中文] 安安\\你好/3 方程式^次方 ! (唐詩三百首) info@gmail.com $1000 %2 18樓-十九 [Chinese]",
        },
    },
    {
        "index": setting.elastic_index_gallery,
        "text": "[中文] 安安\你好/3 方程式^次方 ! (唐詩三百首) info@gmail.com $1000 %2 18樓-十九 [Chinese]",
        "analyzer": AnalyzerEnum.NGRAM.value,
        "answer": {
            " ",
            "-",
            "!",
            ".",
            "(",
            ")",
            "[",
            "]",
            "@",
            "/",
            "\\",
            "%",
            "^",
            "$",
            "0",
            "1",
            "2",
            "3",
            "8",
            "a",
            "c",
            "e",
            "f",
            "g",
            "h",
            "i",
            "l",
            "m",
            "n",
            "o",
            "s",
            "三",
            "中",
            "九",
            "你",
            "十",
            "唐",
            "好",
            "安",
            "式",
            "文",
            "方",
            "樓",
            "次",
            "百",
            "程",
            "詩",
            "首",
        },
    },
    {
        "index": setting.elastic_index_gallery,
        "text": "[中文] 安安\你好/3 方程式^次方 ! (唐詩三百首) info@gmail.com $1000 %2 18樓-十九 [Chinese]",
        "analyzer": AnalyzerEnum.STANDARD.value,
        "answer": {
            "1000",
            "18",
            "2",
            "3",
            "chinese",
            "gmail.com",
            "info",
            "三",
            "中",
            "九",
            "你",
            "十",
            "唐",
            "好",
            "安",
            "式",
            "文",
            "方",
            "樓",
            "次",
            "百",
            "程",
            "詩",
            "首",
        },
    },
    {
        "index": setting.elastic_index_gallery,
        "text": "minio-1://galleries/whatever",
        "analyzer": AnalyzerEnum.URL.value,
        "answer": {
            "minio-1",
            "galleries",
            "whatever",
        },
    },
]


def get_data():
    return [DataModel(**d) for d in raw_data]


def get_tokens(tokens: dict):
    _tokens = set()
    for token in tokens:
        _tokens.add(token["token"])

    return _tokens


@pytest.mark.asyncio(scope="session")
async def test_analyzers(logger: Logger):
    async_elasticsearch = get_async_elasticsearch()
    async with ElasticsearchSession():
        data = get_data()
        for d in data:
            body = {"text": d.text, "analyzer": d.analyzer}
            resp = await async_elasticsearch.indices.analyze(body=body, index=d.index)
            resp_tokens = resp["tokens"]
            tokens = get_tokens(resp_tokens)

            divider()
            logger.debug(f"text: {d.text}")
            logger.debug(f"analyzer: {d.analyzer}")
            logger.debug(f"tokens: {tokens}")
            assert tokens == d.answer
