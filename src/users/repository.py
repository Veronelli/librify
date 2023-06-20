from typing import Any

from src.common.mongo_orm import MongoDB
from bson import ObjectId
from src.config.envs import settings
from src.users.models import User, UserBase

db = MongoDB(
    host="mongodb_librify",
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD
    )

def find_users_by_id(id:str)->dict[str,Any]:
    query = {"_id":ObjectId(id)}
    user = db.find_one("users",query)
    user["_id"] = str(user["_id"])
    
    return user

def register_user(user:UserBase):
    response = db.insert_document("users",user.dict())
    user_response = User(**user.dict(),id=str(response.inserted_id))
    return user_response