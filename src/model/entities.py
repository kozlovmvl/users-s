from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, AfterValidator

from .validators import (
    validate_username_length,
    validate_username_symbols,
    validate_email_struct,
)

Username = Annotated[
    str,
    AfterValidator(validate_username_length),
    AfterValidator(validate_username_symbols),
]
Email = Annotated[
    str,
    AfterValidator(validate_email_struct),
]


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: Username
    email: Email
