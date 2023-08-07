import pytest
from src.users.models import InputUser, UserBase
from src.users.services import create_user as create_user_service, delete_user_by_id

@pytest.fixture
def user_1():
    return {
        "username": "bpitt",
        "email": "bpitt@example.com",
        "is_active": False,
        "password": "TEST1"
    }

@pytest.fixture
def user_2():
    return {
        "username": "jbrave",
        "email": "jbrave@example.com",
        "is_active": False,
        "password": "TEST2"
    }

@pytest.fixture
def user_3():
    return {
        "username": "msmith",
        "email": "msmith@example.com",
        "is_active": False,
        "password": "TEST3"
    }

@pytest.fixture
def create_user():
    async def create(user):
        return await create_user_service(InputUser(**user))
    return create

@pytest.fixture
def delete_user():
    async def delete(id):
        return await delete_user_by_id(id)
    return delete