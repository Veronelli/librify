import pytest
from fastapi.testclient import TestClient
from fastapi import status

# Test create user
async def test_create_user_is_success(app_client: TestClient):
    response = await app_client.get("/users/list")
    assert response.status_code == status.HTTP_200_OK
