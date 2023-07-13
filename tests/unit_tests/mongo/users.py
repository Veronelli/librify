import aiounittest
from unittest.mock import AsyncMock, MagicMock, patch
from src.common.mongo_orm import MongoDB  # Assuming you have a UserRepository class that uses the MongoDB ORM

class UserRepositoryTest(aiounittest.AsyncTestCase):
    async def asyncSetUp(self):
        from src.users import repository as user_repository
        self.mock_orm = MagicMock()
        self.user_repository = user_repository
        self.mongodb = MongoDB(username="root", password="root")

    async def test_get_users(self):
        # Mock the find_documents method of the ORM to return a sample user
        await self.asyncSetUp()
        sample_user = {'name': 'John Doe', 'age': 30,}
        mock_cursor = [sample_user]
        mock_find = AsyncMock()
        mock_find.return_value = mock_cursor
        with patch("src.common.mongo_orm.motor.motor_asyncio.AsyncIOMotorClient",#<===== Check point
                   new={
                        "librify":{
                            "users":[sample_user]
                        }}):
            user = await self.user_repository.find_all_users('users')

        breakpoint()
        self.assertEqual(user, sample_user)

        # Assert that the find_documents method was called with the correct arguments
        self.mock_orm.find_documents.assert_called_once_with('users', {'username': 'john123'})

    async def test_create_user(self):
        # Mock the insert_document method of the ORM to return a sample insert result
        await self.asyncSetUp()

        insert_result = MagicMock()
        self.mock_orm.insert_document.return_value = insert_result

        user_data = {'name': 'John Doe', 'age': 30}
        result = await self.user_repository.register_user(user_data)
        self.assertEqual(result, insert_result)

        # Assert that the insert_document method was called with the correct arguments
        self.mock_orm.insert_document.assert_called_once_with('users', {'username': 'john123', **user_data})

    # Add more test methods for other repository methods

if __name__ == '__main__':
    aiounittest.main()
