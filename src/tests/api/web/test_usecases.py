import pytest
from api.web.usecases import UserUsecase, UserUsecaseProtocol
from api.web.scheme import (
    UserCreateInputSchema,
    UserCreateOutputSchema,
    UserGetOutputSchema,
    UserUpdateInputSchema,
    UserUpdateOutputSchema,
)

from litestar.exceptions import ValidationException


@pytest.mark.asyncio
async def test_usecase_protocol(mock_repo):
    usecase = UserUsecase(repo=mock_repo)
    assert isinstance(usecase, UserUsecaseProtocol)


@pytest.mark.asyncio
async def test_get_by_id(mock_repo, mock_user):
    usecase = UserUsecase(repo=mock_repo)
    result = await usecase.get_by_id(user_id=mock_user)
    assert isinstance(result, UserGetOutputSchema)
    assert result.id == mock_user.id
    assert result.username == mock_user.username
    assert result.email == mock_user.email


@pytest.mark.asyncio
async def test_create_valid_user(mock_repo):
    usecase = UserUsecase(repo=mock_repo)
    input_schema = UserCreateInputSchema(username="user2", email="user2@host")
    result = await usecase.create_user(input_schema)
    assert isinstance(result, UserCreateOutputSchema)
    assert result.username == input_schema.username
    assert result.email == input_schema.email


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_schema",
    [
        UserCreateInputSchema(username="user2!", email="user2@host"),
        UserCreateInputSchema(username="us", email="user2@host"),
        UserCreateInputSchema(username="user2", email="user2"),
    ],
)
async def test_create_invalid_user(mock_repo, input_schema):
    usecase = UserUsecase(repo=mock_repo)
    with pytest.raises(ValidationException):
        await usecase.create_user(input_schema)


@pytest.mark.asyncio
async def test_update_valid_user(mock_repo, mock_user):
    usecase = UserUsecase(repo=mock_repo)
    input_schema = UserUpdateInputSchema(username="user3", email="user3@host")
    result = await usecase.update_user(user_id=mock_user, data=input_schema)
    assert isinstance(result, UserUpdateOutputSchema)
    assert result.id == mock_user.id
    for key, value in input_schema.model_dump().items():
        assert getattr(result, key) == value


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_schema",
    [
        UserUpdateInputSchema(username="user2!", email="user2@host"),
        UserUpdateInputSchema(username="us", email="user2@host"),
        UserUpdateInputSchema(username="user2", email="user2"),
    ],
)
async def test_update_invalid_user(mock_repo, mock_user, input_schema):
    usecase = UserUsecase(repo=mock_repo)
    with pytest.raises(ValidationException):
        await usecase.update_user(user_id=mock_user.id, data=input_schema)


@pytest.mark.asyncio
async def test_delete_user(mock_repo, mock_user):
    usecase = UserUsecase(repo=mock_repo)
    result = await usecase.delete_user(user_id=mock_user.id)
    assert result is None
