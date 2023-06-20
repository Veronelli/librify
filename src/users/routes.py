from typing import Annotated
from fastapi import APIRouter, Body, HTTPException, Path
from bson import ObjectId
from src.config.envs import settings
from src.users.models import User, UserBase
from src.common.mongo_orm import MongoDB
from src.users.repository import find_users_by_id, register_user

route = APIRouter(prefix="/users",tags=["Users"])
db = MongoDB(
    host="mongodb_librify",
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD
    )


@route.get("/{id}")
async def get_user(id:Annotated[str,Path()]):
    user = find_users_by_id(id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(user)
    return User(**user)


@route.post("/register", response_model=User)
def register(user: Annotated[UserBase, Body()])->User:
    return register_user(user)    