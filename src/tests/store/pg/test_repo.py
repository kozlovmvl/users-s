import pytest
from sqlalchemy.sql import exists, select

from model.entities import User
from store.pg.repository import UserRepo
from store.pg.scheme import UserSchema
from store.protocols import UserRepoProtocol


@pytest.mark.asyncio
async def test_repo_protocol(session_maker):
    repo = UserRepo(session_maker=session_maker)
    assert isinstance(repo, UserRepoProtocol)


@pytest.mark.asyncio
async def test_get_user_by_id(session_maker, user_obj):
    repo = UserRepo(session_maker=session_maker)
    user = await repo.get_by_id(user_id=user_obj.id)
    assert user.id == user_obj.id
    assert user.username == user_obj.username
    assert user.email == user_obj.email


@pytest.mark.asyncio
async def test_create_user(session_maker):
    user = User(username="user1", email="name@host")
    repo = UserRepo(session_maker=session_maker)
    result = await repo.create(obj=user)
    assert result is None
    async with session_maker() as session:
        user_from_db = (
            await session.execute(select(UserSchema).where(UserSchema.id == user.id))
        ).scalar_one()
        assert user_from_db.id == user.id
        assert user_from_db.username == user.username
        assert user_from_db.email == user.email


@pytest.mark.asyncio
async def test_update_user(session_maker, user_obj):
    repo = UserRepo(session_maker=session_maker)
    user_obj.username = "user1-changed"
    result = await repo.update(user_obj)
    assert result is None
    async with session_maker() as session:
        user_from_db = (
            await session.execute(
                select(UserSchema).where(UserSchema.id == user_obj.id)
            )
        ).scalar_one()
        assert user_from_db.id == user_obj.id
        assert user_from_db.username == user_obj.username
        assert user_from_db.email == user_obj.email


@pytest.mark.asyncio
async def test_delete_user(session_maker, user_obj):
    repo = UserRepo(session_maker=session_maker)
    result = await repo.delete(user_obj)
    assert result is None
    async with session_maker() as session:
        user_exists = (
            await session.execute(select(exists().where(UserSchema.id == user_obj.id)))
        ).scalar_one()
        assert not user_exists
