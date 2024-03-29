from typing import Annotated

from fastapi import (APIRouter, Body, Depends, HTTPException, Response,
                     status)
from pymongo.errors import WriteError

from src.users.dependencies import verify_token
from src.users.models import InputUser, User, UserBase
from src.users.services import (create_user, delete_user_by_id, get_user,
                                get_users, update_user_by_id)

route = APIRouter(prefix="/users", tags=["Users"])


@route.get("/list/{id}")
async def get(
    user_info: Annotated[
        User, Depends(verify_token(validate_user_equal=True))]):
    user = await get_user(user_info.id)
    if user == []:
        raise HTTPException(status_code=404)
    return user[0]


@route.get("/list")
async def get_all(
        offset: int | None = None,
        limit: int | None = None):
    users = await get_users(offset, limit)
    return users


@route.post("/register", response_model=User)
async def register(user: Annotated[InputUser, Body()]) -> User:
    return await create_user(user)


@route.put("/update/{id}")
async def update(
        user_info: Annotated[
            User,
            Depends(
                verify_token(validate_user_equal=True))],
        user: Annotated[UserBase, Body()]
        ) -> User:
    try:
        return await update_user_by_id(user_info.id, user)
    except WriteError as e:
        raise HTTPException(e.code)


@route.delete("/delete/{id}")
async def delete(
        user_info: Annotated[
            User, Depends(verify_token(validate_user_equal=True))]):
    deleted_user = await delete_user_by_id(user_info.id)

    if deleted_user is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
