import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.account import AccountCreate
from app.services.account import get_account_service, signup_service


@pytest.fixture
async def create_test_account(async_db_session: AsyncSession):
    async def _create_test_account(
        email: str, password: str, fullname: str = "Test User"
    ):
        account_in = AccountCreate(fullname=fullname, email=email, password=password)
        return await signup_service(account_in, async_db_session)

    return _create_test_account


@pytest.mark.asyncio
async def test_create_account(create_test_account):
    account = await create_test_account(
        email="test@example.com", password="password123"
    )
    assert account.email == "test@example.com"
    assert account.fullname == "Test User"


@pytest.mark.asyncio
async def test_get_account_by_email(
    create_test_account, async_db_session: AsyncSession
):
    await create_test_account(email="test@example.com", password="password123")
    account = await get_account_service(email="test@example.com", db=async_db_session)
    assert account is not None
    assert account.email == "test@example.com"
    assert account.fullname == "Test User"


@pytest.mark.asyncio
async def test_get_account_by_id(create_test_account, async_db_session: AsyncSession):
    created_account = await create_test_account(
        email="test@example.com", password="password123"
    )
    account = await get_account_service(
        account_id=created_account.id, db=async_db_session
    )
    assert account is not None
    assert account.id == created_account.id
    assert account.email == "test@example.com"
    assert account.fullname == "Test User"
