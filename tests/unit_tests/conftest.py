import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from main import app
from fastapi.testclient import TestClient
from tests.unit_tests.mock_models import MockDataBaseClient

@pytest.fixture()
def collection_factory():
    return {
        "test":"TEST",
    }

@pytest.fixture
def mock_mongo_motor_client(mocker, collection_factory):
    client_mock = mocker.patch(
        "motor.motor_asyncio.AsyncIOMotorClient",
        return_value=MockDataBaseClient
        )
    breakpoint()
    client_mock.return_value.get_database = mocker.Mock()
    client_mock.return_value.get_database.return_value.get_collection = mocker.Mock(
        side_effect=lambda collection: collection_factory[collection]
    )


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

@pytest.fixture
def app(load_enviroment: None, mock_mongo_motor_client) -> FastAPI:
    from main import app
    return app

@pytest.fixture
async def app_client(app) -> TestClient:
    async with AsyncClient(app=app, base_url="http://localhost") as client:
        yield client

