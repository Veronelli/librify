import datetime
from typing import Any

import bcrypt
import jwt
from bson import ObjectId

from src.config.envs import settings
from src.users.models import LoginUser
from src.users.repository import find
from src.users.session_repository import (exist_token, insert_user_credential,
                                          update_user)


async def login_user(user: LoginUser):
    query = {"email": user.email}
    getted_user = (await find(query=query))[0]
    
    if not bcrypt.checkpw(
        user.password.encode('utf-8'),
        getted_user.password.encode('utf-8')) or not getted_user.is_active:
        return None

    token = jwt.encode(
        getted_user.dict() | 
        {'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
        settings.SECRET_KEY,
        algorithm="HS256")
    
    user_credential = {
        "token": token,
        "user_id": ObjectId(getted_user.id)
    }
    query_id_user_token = {'user_id':ObjectId(getted_user.id)}
    exist_token_user = await exist_token(query_id_user_token) != []
    response: Any
    if (exist_token_user == False):
        response = await insert_user_credential(user_credential)
    else:
        response = await update_user(
            user_credential,
            {
                'user_id': ObjectId(getted_user.id)
            })
    return {'token': token, }