from pytest import mark

@mark.asyncio
async def test_endpoint(client):
    response = await client.get("/users/list")
    assert response.status_code == 200