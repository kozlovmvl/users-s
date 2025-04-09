from uuid import UUID
from model.entities import User
import pytest_asyncio


@pytest_asyncio.fixture()
async def user():
    yield User(username="user1", email="user1@host")


@pytest_asyncio.fixture()
async def mock_repo(user):
    class MockRepo:
        async def get_by_id(self, user_id: UUID, **kwargs) -> User:
            return user

        async def create(self, obj: User, **kwargs) -> None:
            return

        async def update(self, obj: User, **kwargs) -> None:
            return

        async def delete(self, obj: User, **kwargs) -> None:
            return

    yield MockRepo()
