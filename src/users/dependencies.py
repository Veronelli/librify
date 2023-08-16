from typing import Annotated, Any
from fastapi import Depends, HTTPException, status

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.users.models import User, UserBase

from src.users.session_repository import exist_token
from src.users.repository import find_user_by_id

http_bearer = HTTPBearer()


async def check_user(token:Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)])->dict[str,Any]:
    token_getted = await exist_token({"token":token.credentials})
    if token_getted != []:
        user: list[User] = await find_user_by_id(token_getted[0]['user_id'])
        return UserBase(**user[0].dict())
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED
    )
