from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Path, Response
from pymongo.errors import WriteError
from src.users.models import InputUser, User, UserBase
from fastapi import status
from src.users.repository import find_user_by_id, find_all_users, register_user, update_user, delete_user

route = APIRouter(prefix="/users",tags=["Users"])

@route.get("/list/{id}")
async def get(id:Annotated[str,Path()]):
    user = await find_user_by_id(id)
    if user == []:
        raise HTTPException(status_code=404)
    return user[0]

@route.get("/list")
async def get_all(offset:int|None =None,limit:int|None =None):
    users = await find_all_users(offset,limit)
    return users

@route.post("/register", response_model=User)
async def register(user: Annotated[InputUser, Body()])->User:
    return await register_user(user)

@route.put("/update/{id}")
async def update(
    id: Annotated[str,Path()],
    user: Annotated[UserBase, Body()]
    )->User:
    try:
        return await update_user(id, user)
    except WriteError as e:
        raise HTTPException(e.code)
        

@route.delete("/delete/{id}")
async def delete(id:Annotated[str,Path()]):
    deleted_user = await delete_user(id)

    if deleted_user == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
