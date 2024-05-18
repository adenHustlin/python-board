import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account import AccountRepository
from app.schemas.account import AccountCreate
from app.services.auth import authenticate_account, create_session, destroy_session


@pytest.fixture
async def create_test_account(async_db_session: AsyncSession):
    async def _create_test_account(
        email: str, password: str, fullname: str = "Test User"
    ):
        account_in = AccountCreate(fullname=fullname, email=email, password=password)
        return await AccountRepository.create(async_db_session, account_in)

    return _create_test_account


@pytest.mark.asyncio
async def test_authenticate_account(
    create_test_account, async_db_session: AsyncSession
):
    await create_test_account(email="test@example.com", password="password123")
    account = await authenticate_account(
        async_db_session, "test@example.com", "password123"
    )
    assert account is not None


@pytest.mark.asyncio
async def test_create_session(create_test_account, async_db_session: AsyncSession):
    account_in = await create_test_account(
        email="test@example.com", password="password123"
    )
    access_token = await create_session(account_in.id)
    assert access_token is not None


@pytest.mark.asyncio
async def test_destroy_session(create_test_account, async_db_session: AsyncSession):
    account_in = await create_test_account(
        email="test@example.com", password="password123"
    )
    await create_session(account_in.id)
    await destroy_session(account_in.id)
