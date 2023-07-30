import pytest

from tests.unit_tests.interfaces import IAsyncIOMotorClient
from tests.unit_tests.mock_collection.user_collection import MockUserCollection


@pytest.fixture
def collection_factory():
    return {
        "librify":{
            'users': MockUserCollection
        },
    }


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"

@pytest.fixture
def mock_mongo_motor_client(mocker, collection_factory):
    mock_db = mocker.Mock()
    client_mock = mocker.patch(
        "motor.motor_asyncio",
        return_value=mock_db
        )
    client_mock.AsyncIOMotorClient.return_value = collection_factory
    return client_mock