import pytest
from src.users.models import UserBase
from src.users.repository import register_user, delete_user as delete_use_repo

@pytest.fixture
def user_1():
    return {
        "username": "bpitt",
        "email": "bpitt@example.com",
        "is_active": False
    }

@pytest.fixture
def user_2():
    return {
        "username": "jbrave",
        "email": "jbrave@example.com",
        "is_active": False
    }

@pytest.fixture
def user_3():
    return {
        "username": "msmith",
        "email": "msmith@example.com",
        "is_active": False
    }

@pytest.fixture
def create_user():
    async def create(user):
        return await register_user(UserBase(**user))
    return create

@pytest.fixture
def delete_user():
    async def delete(id):
        return await delete_use_repo(id)
    return delete