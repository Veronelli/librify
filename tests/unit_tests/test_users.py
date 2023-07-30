from typing import Any
from fastapi.testclient import TestClient
from fastapi import status
import pytest


# Test create user
@pytest.mark.anyio
async def test_create_user_is_success(app_client: TestClient, mock_mongo_motor_client, mocked_users: list[dict[str, Any]]):
    response = await app_client.get("/users/list")
    assert response.status_code == status.HTTP_200_OK

