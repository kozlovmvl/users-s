from typing import Protocol, runtime_checkable
from uuid import UUID

from litestar.exceptions import ValidationException

from api.web.scheme import (
    UserCreateInputSchema,
    UserCreateOutputSchema,
    UserGetOutputSchema,
    UserUpdateInputSchema,
    UserUpdateOutputSchema,
)
from model.entities import User
from model.exceptions import (
    EmailInvalidStruct,
    UsernameInvalidLength,
    UsernameInvalidSymbol,
)
from store.protocols import UserRepoProtocol


@runtime_checkable
class UserUsecaseProtocol(Protocol):
    async def get_by_id(self, user_id: UUID) -> UserGetOutputSchema: ...

    async def create_user(
        self, data: UserCreateInputSchema
    ) -> UserCreateOutputSchema: ...

    async def update_user(
        self, user_id: UUID, data: UserUpdateInputSchema
    ) -> UserUpdateOutputSchema: ...

    async def delete_user(self, user_id: UUID) -> None: ...


class UserUsecase:
    def __init__(self, repo: UserRepoProtocol):
        self.repo = repo

    async def get_by_id(self, user_id: UUID) -> UserGetOutputSchema:
        user = await self.repo.get_by_id(user_id=user_id)
        return UserGetOutputSchema.model_validate(user)

    async def create_user(self, data: UserCreateInputSchema) -> UserCreateOutputSchema:
        try:
            user = User.model_validate(data)
        except (
            UsernameInvalidLength,
            UsernameInvalidSymbol,
            EmailInvalidStruct,
        ) as err:
            raise ValidationException from err
        await self.repo.create(user)
        return UserCreateOutputSchema.model_validate(user)

    async def update_user(
        self, user_id: UUID, data: UserUpdateInputSchema
    ) -> UserUpdateOutputSchema:
        user = await self.repo.get_by_id(user_id=user_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            try:
                setattr(user, key, value)
            except (
                UsernameInvalidLength,
                UsernameInvalidSymbol,
                EmailInvalidStruct,
            ) as err:
                raise ValidationException from err
        await self.repo.update(user)
        return UserUpdateOutputSchema.model_validate(user)

    async def delete_user(self, user_id: UUID) -> None:
        user = await self.repo.get_by_id(user_id=user_id)
        await self.repo.delete(user)
