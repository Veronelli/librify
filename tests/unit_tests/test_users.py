from typing import Any

import pytest
from bson import ObjectId
from fastapi import status
from fastapi.testclient import TestClient


# Test create user
@pytest.mark.anyio
async def test_list_user_is_success(
        app_client: TestClient,
        mocked_users: list[dict[str, Any]]):
    response = await app_client.get("/users/list")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == mocked_users


@pytest.mark.anyio
async def test_get_user_is_success(
        app_client: TestClient,
        mocked_users: list[dict[str, Any]]):
    users = mocked_users[1]
    response = await app_client.get(f"/users/list/{users['_id']}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == users


@pytest.mark.anyio
async def test_get_user_is_failed_due_invalid_id(
        app_client: TestClient):
    response = await app_client.get(f"/users/list/{ObjectId()}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_register_user_is_success(
        app_client: TestClient,
        create_user: dict[str, Any]):
    user = create_user
    response = await app_client.post(
        "/users/register",
        json=user)
    content = response.json()
    del content['_id']
    assert response.status_code == status.HTTP_200_OK
    assert content == user


@pytest.mark.anyio
async def test_register_user_is_failed_due_bad_request(
        app_client: TestClient,
        bad_payload):
    user = bad_payload
    response = await app_client.post(
        "/users/register",
        json=user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_update_user_is_success(
        app_client: TestClient,
        mocked_users,
        create_user: dict[str, Any]):
    user = create_user
    response = await app_client.put(
        f"/users/update/{mocked_users[2]['_id']}",
        json=user)
    content = response.json()
    user['_id'] = mocked_users[2]['_id']
    assert response.status_code == status.HTTP_200_OK
    assert content == user


@pytest.mark.anyio
async def test_update_user_is_failed_due_not_found_or_not_updated(
        app_client: TestClient, create_user: dict[str, Any]):
    user = create_user
    response = await app_client.put(
        f"/users/update/{str(ObjectId())}",
        json=user)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_delete_user_is_success(app_client, mocked_users):
    user = mocked_users[1]
    response = await app_client.delete(f"/users/delete/{user['_id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.anyio
async def test_delete_user_is_failed_due_not_found_user(app_client):
    response = await app_client.delete(f"/users/delete/{str(ObjectId())}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
