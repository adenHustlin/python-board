import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.account import create_account, get_account_by_email
from app.schemas.account import AccountCreate


@pytest.mark.asyncio
async def test_create_account(async_db_session: AsyncSession):
    account_in = AccountCreate(
        fullname="Test Account", email="test@example.com", password="password123"
    )
    account = await create_account(async_db_session, account_in)
    assert account.email == "test@example.com"
    assert account.fullname == "Test Account"


@pytest.mark.asyncio
async def test_get_account_by_email(async_db_session: AsyncSession):
    account_in = AccountCreate(
        fullname="Test Account", email="test@example.com", password="password123"
    )
    await create_account(async_db_session, account_in)
    account = await get_account_by_email(async_db_session, "test@example.com")
    assert account is not None
    assert account.email == "test@example.com"
    assert account.fullname == "Test Account"
