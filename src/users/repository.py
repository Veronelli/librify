from typing import Any

from src.common.mongo_orm import connectMongoDB
from pymongo.results import InsertOneResult
from pymongo.errors import WriteError
from bson import ObjectId
from fastapi import status
from src.users.models import InputUser, User, UserBase
from bson import ObjectId



async def find(query: dict[str,Any]|None=None,):
    db = connectMongoDB()
    users_response = await db.find_documents("users", query=query)
    users = [user for user in users_response]
    for user in users:
        user["_id"] = str(user["_id"])

    return [User(**user) for user in users]

async def find_user_by_id(id: str) -> dict[str, Any]:
    """
    Find a user by their ID.

    Args:
        id (str): The ID of the user.

    Returns:
        dict[str, Any]: The user document as a dictionary.
    """
    query = {'_id': ObjectId(id)}
    return await find(query=query)


async def find_all_users(offset: int | None = None, limit: int | None = None) -> list[User]:
    """
    Find all users.

    Args:
        offset (int | None, optional): The number of documents to skip. Defaults to None.
        limit (int | None, optional): The maximum number of documents to return. Defaults to None.

    Returns:
        list[User]: A list of User objects.
    """
    return await find()

async def register_user(user: InputUser) -> dict[str, Any]:
    """
    Register a new user.

    Args:
        user (UserBase): The user data.

    Returns:
        dict[str, Any]: The response containing the inserted user document.
    """
    db = connectMongoDB()
    response: InsertOneResult = await db.insert_document("users", user.dict())
    user_response = User(**user.dict(), _id=str(response.inserted_id))
    return user_response

async def update_user(id: str, user: UserBase) -> dict[str, Any]:
    """
    Update a user.

    Args:
        id (str): The ID of the user.
        user (UserBase): The user data.

    Returns:
        dict[str, Any]: The response containing the updated user document.
    """
    db = connectMongoDB()

    query = {"_id": ObjectId(id)}
    updated = await db.update_document("users", query, user.dict(by_alias=True))
    if not updated.raw_result['updatedExisting']:
        raise WriteError(code=status.HTTP_404_NOT_FOUND, error="Not found user")
    user_response = User(**user.dict(by_alias=True), _id=id)
    return user_response

async def delete_user(id: str) -> dict[str, Any]:
    """
    Delete a user.

    Args:
        id (str): The ID of the user.

    Returns:
        dict[str, Any]: The response containing the deleted user document.
    """
    db = connectMongoDB()

    query = {"_id": ObjectId(id)}
    response = await db.delete_document("users", query)
    return response.deleted_count > 0
