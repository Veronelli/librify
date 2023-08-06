from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Path, Response
from pymongo.errors import WriteError
from src.users.models import InputUser, User, UserBase
from fastapi import status
from src.users.services import get_users, get_user, create_user, update_user_by_id, delete_user_by_id

route = APIRouter(prefix="/users",tags=["Users"])

@route.get("/list/{id}")
async def get(id:Annotated[str,Path()]):
    user = await get_user(id)
    if user == []:
        raise HTTPException(status_code=404)
    return user[0]

@route.get("/list")
async def get_all(offset:int|None =None,limit:int|None =None):
    users = await get_users(offset,limit)
    return users

@route.post("/register", response_model=User)
async def register(user: Annotated[InputUser, Body()])->User:
    return await create_user(user)

@route.put("/update/{id}")
async def update(
    id: Annotated[str,Path()],
    user: Annotated[UserBase, Body()]
    )->User:
    try:
        return await update_user_by_id(id, user)
    except WriteError as e:
        raise HTTPException(e.code)
        

@route.delete("/delete/{id}")
async def delete(id:Annotated[str,Path()]):
    deleted_user = await delete_user_by_id(id)

    if deleted_user == False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
