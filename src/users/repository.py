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


def find_user_by_id(id: str) -> dict[str, Any]:
    """
    Find a user by their ID.

    Args:
        id (str): The ID of the user.

    Returns:
        dict[str, Any]: The user document as a dictionary.
    """
    query = {"_id": ObjectId(id)}
    user = db.find_one("users", query)
    user["_id"] = str(user["_id"])
    return user


def find_all_users(offset: int | None = None, limit: int | None = None) -> list[User]:
    """
    Find all users.

    Args:
        offset (int | None, optional): The number of documents to skip. Defaults to None.
        limit (int | None, optional): The maximum number of documents to return. Defaults to None.

    Returns:
        list[User]: A list of User objects.
    """
    users_response = db.find_documents("users", offset=offset, limit=limit)
    users = [user for user in users_response]
    for user in users:
        user["_id"] = str(user["_id"])
    return [User(**user) for user in users]


def register_user(user: UserBase) -> dict[str, Any]:
    """
    Register a new user.

    Args:
        user (UserBase): The user data.

    Returns:
        dict[str, Any]: The response containing the inserted user document.
    """
    response = db.insert_document("users", user.dict())
    user_response = User(**user.dict(), id=str(response.inserted_id))
    return user_response