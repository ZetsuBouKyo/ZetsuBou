from back.model.elasticsearch import ElasticsearchAnalyzerEnum


def test_elasticsearch_analyzer_enum():
    assert ElasticsearchAnalyzerEnum.DEFAULT == ElasticsearchAnalyzerEnum.DEFAULT.value
