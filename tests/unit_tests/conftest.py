import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient


pytest_plugins = [
    "tests.unit_tests.fixtures.user_fixtures",
    "tests.unit_tests.fixtures.mongo_fixtures"
]


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


@pytest.fixture
def load_enviroment(monkeypatch):
    monkeypatch.setenv(
        "MONGO_INITDB_ROOT_USERNAME",
        "TEST_USERNAME"
        )
    monkeypatch.setenv(
        "MONGO_INITDB_ROOT_PASSWORD",
        "TEST_PASSWORD"
        )
    monkeypatch.setenv(
        "SECRET_KEY",
        "SECRET_KEY"
        )


@pytest.fixture(name="app")
def app_fixture(load_enviroment: None) -> FastAPI:
    from main import app
    return app


@pytest.fixture
async def app_client(app) -> TestClient:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client
