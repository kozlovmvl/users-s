from uuid import UUID

from sqlalchemy.sql import delete, select

from model.entities import User
from store.pg.core import async_session_maker
from store.pg.scheme import UserSchema


class UserRepo:
    def __init__(self, session_maker=async_session_maker):
        self.session_maker = session_maker

    async def get_by_id(self, user_id: UUID, **kwargs) -> User:
        stmt = select(UserSchema).where(UserSchema.id == user_id)
        async with self.session_maker() as session:
            user_schema = (await session.execute(stmt)).scalar_one()
            return user_schema.to_model()

    async def create(self, obj: User, **kwargs) -> None:
        user_schema = UserSchema.from_model(obj)
        async with self.session_maker() as session:
            session.add(user_schema)
            await session.commit()

    async def update(self, obj: User, **kwargs) -> None:
        stmt = select(UserSchema).where(UserSchema.id == obj.id)
        async with self.session_maker() as session:
            user_schema = (await session.execute(stmt)).scalar_one()
            user_schema.username = obj.username
            await session.commit()

    async def delete(self, obj: User, **kwargs) -> None:
        stmt = delete(UserSchema).where(UserSchema.id == obj.id)
        async with self.session_maker() as session:
            await session.execute(stmt)
