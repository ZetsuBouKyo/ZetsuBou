import pytest

from command.redis import _list_pairs, flushall, get, list, ping, set
from lib.faker import ZetsuBouFaker
from tests.general.cli import cli_runner
from tests.general.session import BaseIntegrationSession


@pytest.mark.asyncio(scope="session")
async def test_ping():
    async with BaseIntegrationSession():
        await cli_runner(ping)


@pytest.mark.asyncio(scope="session")
async def test_crud():
    async with BaseIntegrationSession():
        faker = ZetsuBouFaker()
        key = f"test-{faker.random_string(8)}"
        value = faker.random_string(20)
        args_set = [key, value]
        await cli_runner(set, args_set)

        args_get = [key]
        gotten_value = await cli_runner(get, args_get)
        assert gotten_value == value

        pairs = await cli_runner(_list_pairs, ["*"])
        for k, v in pairs:
            if k == key and v == value:
                break
        else:
            assert False, f"key: {key} and value: {value} not found"

        await cli_runner(flushall)
        keys = await cli_runner(list, ["*"])
        assert len(keys) == 0
