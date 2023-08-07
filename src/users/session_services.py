import datetime
from src.config.envs import settings
from src.users.repository import find
from src.users.models import LoginUser
import bcrypt
import jwt

async def login_user(user: LoginUser):
    getted_user = (await find({"email": user.email}))[0]

    if not bcrypt.checkpw(
        user.password.encode('utf-8'),
        getted_user.password.encode('utf-8')):
        return None
    
    token = jwt.encode(
        getted_user.dict() | 
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
        settings.SECRET_KEY,
        algorithm="HS256")
    return {'token': token}