from pytest import mark
from fastapi import status
import asyncio

@mark.asyncio
async def test_endpoint(client, user_1, user_2, user_3, create_user, delete_user):
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
