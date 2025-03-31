import pytest
from model.entities import User
from model.exceptions import (
    EmailInvalidStruct,
    UsernameInvalidLength,
    UsernameInvalidSymbol,
)


def test_valid_user():
    user = User(
        username="username",
        email="name@host",
    )
    assert user


def test_invalid_user():
    with pytest.raises(UsernameInvalidLength):
        _ = User(
            username="1",
            email="name@host",
        )

    with pytest.raises(UsernameInvalidSymbol):
        _ = User(
            username="@abc",
            email="name@host",
        )

    with pytest.raises(EmailInvalidStruct):
        _ = User(
            username="username",
            email="12",
        )
