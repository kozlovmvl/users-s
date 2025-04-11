from uuid import UUID
from pydantic import BaseModel


class UserGetOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str

    model_config = {"from_attributes": True}


class UserCreateInputSchema(BaseModel):
    username: str
    email: str

    model_config = {"from_attributes": True}


class UserCreateOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str

    model_config = {"from_attributes": True}


class UserUpdateInputSchema(BaseModel):
    username: str | None = None
    email: str | None = None

    model_config = {"from_attributes": True}


class UserUpdateOutputSchema(BaseModel):
    id: UUID
    username: str
    email: str

    model_config = {"from_attributes": True}
