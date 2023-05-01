import pytest
from back.session.health import is_airflow_healthy, is_elasticsearch_healthy


@pytest.mark.asyncio
async def test_airflow_health():
    res = await is_airflow_healthy()
    assert res, "airflow is not healthy"


@pytest.mark.asyncio
async def test_elasticsearch_health():
    res = await is_elasticsearch_healthy()
    assert res, "elasticsearch is not healthy"
