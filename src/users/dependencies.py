from typing import Annotated, Any

from bson import ObjectId
from fastapi import Depends, HTTPException, Path, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.users.models import User
from src.users.repository import find_user_by_id
from src.users.session_repository import exist_token

http_bearer = HTTPBearer()


def verify_token(validate_user_equal: bool = False):
    async def check_user(
            token: Annotated[
                HTTPAuthorizationCredentials,
                Depends(http_bearer)],
            id: Annotated[str | None, Path()]
            ) -> dict[str, Any]:
        token_getted = await exist_token({"token": token.credentials})
        if (
                (
                    validate_user_equal and
                    token_getted[0]["user_id"] != ObjectId(id))
                or
                (token_getted == [])):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND)

        user: list[User] = await find_user_by_id(token_getted[0]['user_id'])
        return user[0]

    return check_user
