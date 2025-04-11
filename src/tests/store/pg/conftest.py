from contextlib import asynccontextmanager

import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from model.entities import User
from store.pg.core import Base
from store.pg.scheme import UserSchema
from tests.settings import settings


@pytest_asyncio.fixture()
async def session_maker():
    engine = create_async_engine(url=settings.get_db_url())
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        session = async_sessionmaker(bind=connection, expire_on_commit=False)()

        @asynccontextmanager
        async def create_session():
            yield session

        yield create_session
        await connection.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def user_obj(session_maker):
    user = User(username="user1", email="user1@host")
    user_schema = UserSchema.from_model(user)
    async with session_maker() as session:
        session.add(user_schema)
        await session.commit()
    yield user
