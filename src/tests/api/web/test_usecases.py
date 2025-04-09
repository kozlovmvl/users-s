import pytest
from api.web.usecases import UserUsecase, UserUsecaseProtocol


@pytest.mark.asyncio
async def test_usecase_protocol(mock_repo):
    repo = UserUsecase(repo=mock_repo)
    assert isinstance(repo, UserUsecaseProtocol)
