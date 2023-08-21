import bcrypt

from src.config.envs import settings
from src.users.models import InputUser
from src.users.repository import (delete_user, find_all_users, find_user_by_id,
                                  register_user, update_user)


async def get_users(
    offset:int|None=None,
    limit:int|None =None):
    return await find_all_users(offset,limit)

async def get_user(id):
    return await find_user_by_id(id)

async def create_user(user: InputUser):
    salt = bcrypt.gensalt()
    user.password = (
        bcrypt.hashpw(
        password=user.password.encode('utf-8'),
        salt=salt)
        )
    
    return await register_user(user)

async def update_user_by_id(
    id,
    user):
    return await update_user(id, user)

async def delete_user_by_id(id):
    return await delete_user(id)
