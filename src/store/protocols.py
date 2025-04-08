from typing import Protocol, runtime_checkable
from uuid import UUID

from model.entities import User


@runtime_checkable
class UserRepoProtocol(Protocol):
    async def get_by_id(self, user_id: UUID, **kwargs) -> User: ...

    async def create(self, obj: User, **kwargs) -> None: ...

    async def update(self, obj: User, **kwargs) -> None: ...

    async def delete(self, obj: User, **kwargs) -> None: ...
