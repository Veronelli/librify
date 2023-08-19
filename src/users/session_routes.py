from fastapi import APIRouter, HTTPException, status

from src.users.models import LoginUser
from src.users.session_services import login_user

route = APIRouter(prefix="/session", tags=["UsersSession"])


@route.post("/login")
async def login(user: LoginUser):
    token = await login_user(user)

    if token is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return token
