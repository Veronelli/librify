import asyncio
from typing import Any, Callable, Coroutine

from bson import ObjectId
from fastapi import status
from httpx import AsyncClient
from pytest import mark

from src.users.models import LoginUser
from src.users.session_services import login_user


@mark.asyncio
async def test_list_users(
        client,
        user_1: dict[str, Any],
        user_2: dict[str, Any],
        user_3: dict[str, Any],
        create_user: Callable[..., Coroutine[Any, Any, dict[str, Any]]],
        delete_user: Callable[..., Coroutine[Any, Any, dict[str, Any]]]):
    create_user1 = await create_user(user_1)
    create_user2 = await create_user(user_2)
    create_user3 = await create_user(user_3)

    user_1["id"] = create_user1
    user_2["id"] = create_user2
    user_3["id"] = create_user3

    response = await client.get("/users/list")
    try:
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            create_user1.dict(by_alias=True),
            create_user2.dict(by_alias=True),
            create_user3.dict(by_alias=True)]
    finally:
        d1 = delete_user(create_user1.id)
        d2 = delete_user(create_user2.id)
        d3 = delete_user(create_user3.id)

        asyncio.gather(d1, d2, d3)


@mark.asyncio
async def test_user_detail(
        client,
        user_1: dict[str, Any],
        user_2: dict[str, Any],
        create_user: Callable[..., Coroutine[Any, Any, dict[str, Any]]],
        delete_user: Callable[..., Coroutine[Any, Any, dict[str, Any]]]):
    create_user1 = await create_user(user_1)
    create_user2 = await create_user(user_2)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])
    token = await login_user(payload)

    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
            }
        response = await client.get(
            f"/users/list/{str(create_user1.id)}",
            headers=headers
        ),
        assert response[0].status_code == status.HTTP_200_OK
        assert create_user1.dict(by_alias=True) == response[0].json()
    finally:
        d1 = delete_user(create_user1.id)
        d2 = delete_user(create_user2.id)

        asyncio.gather(d1, d2, )


@mark.asyncio
async def test_user_detail_is_not_authorized(
        client,
        user_1: dict[str, Any],
        create_user: Callable[..., Coroutine[Any, Any, dict[str, Any]]],
        delete_user: Callable[..., Coroutine[Any, Any, dict[str, Any]]]):
    create_user1 = await create_user(user_1)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])
    token = await login_user(payload)

    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
        }
        response = await client.get(
            f"/users/list/{str(ObjectId())}",
            headers=headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
    finally:
        d1 = delete_user(create_user1.id)

        asyncio.gather(d1)


@mark.asyncio
async def test_register_user(client: AsyncClient, delete_user):
    response = await client.post(
        "/users/register",
        json={
            "username": "string",
            "email": "user@example.com",
            "is_active": False,
            "password": "TEST1"
            }
        )

    try:
        assert response.status_code == status.HTTP_200_OK
    finally:
        await delete_user(response.json()['_id'])


@mark.asyncio
async def test_register_user_is_failed_due_bad_request(
        client: AsyncClient):
    response = await client.post(
        "/users/register",
        json={
                "username": "string",
                "is_active": False
            }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@mark.asyncio
async def test_update_user(
        client,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])
    token = await login_user(payload)

    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
        }

        response = await client.put(
            f"/users/update/{create_user1.id}",
            json={
                "username": "string",
                "email": "user@example.com",
                "password": "TEST1"
            },
            headers=headers
            )
        assert response.status_code == status.HTTP_200_OK

    finally:
        await delete_user(create_user1.id)


@mark.asyncio
async def test_update_user_is_failed_due_not_found_user(
        client,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])

    token = await login_user(payload)

    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
        }
        response = await client.put(
            f"/users/update/{str(ObjectId())}",
            json={
                "username": "string",
                "email": "user@example.com",
            },
            headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    finally:
        await delete_user(create_user1.id)


@mark.asyncio
async def test_update_user_is_failed_due_incorrect_authentication(
        client,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])

    token = await login_user(payload)

    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
        }
        response = await client.put(
            f"/users/update/{str(ObjectId())}",
            json={
                "username": "string",
            },
            headers=headers)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    finally:
        await delete_user(create_user1.id)


@mark.asyncio
async def test_delete_user(
        client,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])

    token = await login_user(payload)
    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
        }
        response = await client.delete(
            f"/users/delete/{create_user1.id}",
            headers=headers
            )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    finally:
        await delete_user(create_user1.id)


@mark.asyncio
async def test_delete_user_is_failed_due_not_found_user(
        client,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    payload = LoginUser(
        email=user_1["email"],
        password=user_1["password"])

    token = await login_user(payload)
    headers = {
        'Authorization': f'Bearer {token["token"]}'
    }
    try:
        assert token is not None
        headers = {
            'Authorization': f'Bearer {token["token"]}'
        }
        response = await client.delete(
            f"/users/delete/{str(ObjectId())}",
            headers=headers
            )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    finally:
        await delete_user(create_user1.id)


@mark.asyncio
async def test_login_user(
        client: AsyncClient,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    try:
        response = await client.post(
            url="/session/login",
            json={
                "email": "bpitt@example.com",
                "password": "TEST1",
            })
        assert response.status_code == status.HTTP_200_OK

    finally:
        await delete_user(create_user1.id)


@mark.asyncio
async def test_login_user_is_failed_due_invalid_credential(
        client: AsyncClient,
        user_1: dict[str, Any],
        create_user,
        delete_user):
    create_user1 = await create_user(user_1)
    try:
        response = await client.post(
            url="/session/login",
            json={
                "email": "bpitt@example.com",
                "password": "TEST2",
            })
        assert response.status_code == status.HTTP_404_NOT_FOUND

    finally:
        await delete_user(create_user1.id)
