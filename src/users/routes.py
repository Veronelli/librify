from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Path, Query
from bson import ObjectId
from src.config.envs import settings
from src.users.models import User, UserBase
from src.common.mongo_orm import MongoDB
from src.users.repository import find_user_by_id, find_all_users, register_user, update_user, delete_user

route = APIRouter(prefix="/users",tags=["Users"])
db = MongoDB(
    host="mongodb_librify",
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD
    )


@route.get("/list/{id}")
async def get_all(id:Annotated[str,Path()]):
    user = await find_user_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**user)

@route.get("/list")
async def get(offset:int|None =None,limit:int|None =None):
    users = await find_all_users(offset,limit)
    return users

@route.post("/register", response_model=User)
def register(user: Annotated[UserBase, Body()])->User:
    return register_user(user)

@route.put("/update/{id}")
def update(id:Annotated[str,Path()],user: Annotated[UserBase, Body()])->User:
    return update_user(id,user)

@route.delete("/delete/{id}")
def delete(id:Annotated[str,Path()]):
    deleted_user = delete_user(id)
    return {
        "message":"User deleted",
        "user": deleted_user
    }
