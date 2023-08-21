import pytest

from tests.unit_tests.mock_collection.user_collection import MockUserCollection


@pytest.fixture
def collection_factory():
    return {
        "librify": {
            'users': MockUserCollection()
        },
    }


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
