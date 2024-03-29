import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient

pytest_plugins = [
    "tests.integration_tests.fixtures.user_fixtures",
]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def app():
    from main import app as application
    return application


@pytest_asyncio.fixture
async def client(app):
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client
