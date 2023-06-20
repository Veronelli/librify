from typing import Annotated
from fastapi import APIRouter, Body
from bson import ObjectId
from src.config.envs import settings

from src.users.models import User, UserBase
from src.common.mongo_orm import MongoDB

route = APIRouter(prefix="/users")
db = MongoDB(
    host="mongodb_librify",
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD
    )

@route.post("/register", response_model=User)
def register_user(user: Annotated[UserBase, Body()])->User:
    print(user.dict())
    response =  db.insert_document("users",user.dict())
    user_response = User(**user.dict(),id=str(response.inserted_id))
    return user_response
    