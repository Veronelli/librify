from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Path, Query
from bson import ObjectId
from src.config.envs import settings
from src.users.models import User, UserBase
from src.common.mongo_orm import MongoDB
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
async def register(user: Annotated[UserBase, Body()])->User:
    return await register_user(user)

@route.put("/update/{id}")
async def update(
    id: Annotated[str,Path()],
    user: Annotated[UserBase, Body()]
    )->User:
    return await update_user(id, user)

@route.delete("/delete/{id}")
async def delete(id:Annotated[str,Path()]):
    deleted_user = await delete_user(id)
    return {
        "message":"User deleted",
        "user": deleted_user
    }
