import pytest

from tests.unit_tests.fixtures.results.users_results import (MOCKED_USER_1,
                                                             MOCKED_USER_2,
                                                             MOCKED_USER_3,
                                                             MOCKED_USER_4)


@pytest.fixture
def mocked_users():
    return [MOCKED_USER_1, MOCKED_USER_2, MOCKED_USER_3]

@pytest.fixture
def create_user():
    return MOCKED_USER_4

@pytest.fixture
def bad_payload():
    return {
        "email": "ncuevas@example.com",
        "is_active": True,
    }