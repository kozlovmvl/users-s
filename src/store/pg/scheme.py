from datetime import datetime
from typing import Self
from uuid import UUID

from sqlalchemy import UUID as SQLA_UUID
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from model.entities import User
from store.pg.core import Base


class UserSchema(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(SQLA_UUID, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    def to_model(self) -> User:
        return User(id=self.id, username=self.username, email=self.email)

    @classmethod
    def from_model(cls, obj: User) -> Self:
        return UserSchema(id=obj.id, username=obj.username, email=obj.email)
