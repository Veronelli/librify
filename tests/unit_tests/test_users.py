from typing import Any
from fastapi.testclient import TestClient
from fastapi import status
import pytest
from bson import ObjectId

# Test create user
@pytest.mark.anyio
async def test_list_user_is_success(app_client: TestClient, mock_mongo_motor_client, mocked_users: list[dict[str, Any]]):
    response = await app_client.get("/users/list")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mocked_users


@pytest.mark.anyio
async def test_get_user_is_success(app_client: TestClient, mock_mongo_motor_client, mocked_users: list[dict[str, Any]]):
    users = mocked_users[1]
    response = await app_client.get(f"/users/list/{users['_id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == users

@pytest.mark.anyio
async def test_get_user_is_failed_due_invalid_id(app_client: TestClient, mock_mongo_motor_client, mocked_users: list[dict[str, Any]]):
    users = mocked_users[0]
    response = await app_client.get(f"/users/list/{ObjectId()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

