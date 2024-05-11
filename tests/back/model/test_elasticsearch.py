from back.model.elasticsearch import ElasticsearchAnalyzerEnum


def test_elasticsearch_analyzer_enum():
    assert ElasticsearchAnalyzerEnum.DEFAULT == ElasticsearchAnalyzerEnum.DEFAULT.value


def test_elasticsearch_analyzer_enum():
    d = {ElasticsearchAnalyzerEnum.DEFAULT: 1}
    assert d.get(ElasticsearchAnalyzerEnum.DEFAULT.value, None) == 1
    assert d.get(ElasticsearchAnalyzerEnum.DEFAULT, None) == 1

    d = {ElasticsearchAnalyzerEnum.DEFAULT.value: 1}
    assert d.get(ElasticsearchAnalyzerEnum.DEFAULT.value, None) == 1
    assert d.get(ElasticsearchAnalyzerEnum.DEFAULT, None) == 1
