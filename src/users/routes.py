from fastapi import APIRouter
from src.config.envs import settings

from src.users.models import User
from src.common.mongo_orm import MongoDB

route = APIRouter(prefix="/users")
db = MongoDB(
    host="mongodb_librify",
    username=settings.MONGO_INITDB_ROOT_USERNAME,
    password=settings.MONGO_INITDB_ROOT_PASSWORD
    )

@route.post("/register")
async def register_user():
    return await db.insert_document("users",{
        "username": "Facundo",
        "password": "Nose XD"
    })

    