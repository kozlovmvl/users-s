from uuid import UUID
from pydantic import BaseModel


class UserGetOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str


class UserCreateInputSchema(BaseModel):
    username: str
    email: str


class UserCreateOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str


class UserUpdateInputSchema(BaseModel):
    username: str | None = None
    email: str | None = None


class UserUpdateOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str
