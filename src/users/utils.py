from typing import Any
from bson import ObjectId

from src.common.mongo_orm import connectMongoDB
from src.config.envs import settings

async def find_user(id: str) -> dict[str, Any]:
    """
    Find a user by their ID.

    Args:
        id (str): The ID of the user.

    Returns:
        dict[str, Any]: The user document as a dictionary.
    """
    db = connectMongoDB()
    query = {"_id": ObjectId(id)}
    users = await db.find_documents("users", query)
    for user in users:
        user["_id"] = str(user["_id"])
        return user
