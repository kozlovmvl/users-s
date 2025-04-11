from uuid import UUID

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from api.web.scheme import (
    UserCreateInputSchema,
    UserCreateOutputSchema,
    UserGetOutputSchema,
    UserUpdateInputSchema,
    UserUpdateOutputSchema,
)
from api.web.usecases import UserUsecase, UserUsecaseProtocol
from store.pg.repository import UserRepo


async def provide_usecase() -> UserUsecaseProtocol:
    return UserUsecase(repo=UserRepo())


class UserController(Controller):
    path = "user"
    dependencies = {
        "usecase": Provide(provide_usecase),
    }

    @get("{user_id:uuid}")
    async def get_by_id(
        self, user_id: UUID, usecase: UserUsecaseProtocol
    ) -> UserGetOutputSchema:
        return await usecase.get_by_id(user_id=user_id)

    @post("")
    async def create(
        self, data: UserCreateInputSchema, usecase: UserUsecaseProtocol
    ) -> UserCreateOutputSchema:
        return await usecase.create_user(data=data)

    @patch("{user_id:uuid}")
    async def patch(
        self, user_id: UUID, data: UserUpdateInputSchema, usecase: UserUsecaseProtocol
    ) -> UserUpdateOutputSchema:
        return await usecase.update_user(user_id=user_id, data=data)

    @delete("{user_id:uuid}")
    async def delete(self, user_id: UUID, usecase: UserUsecaseProtocol) -> None:
        return await usecase.delete_user(user_id=user_id)
