import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.account import create_account
from app.schemas.account import AccountCreate
from app.services.auth import authenticate_account, create_session


@pytest.mark.asyncio
async def test_authenticate_account(async_db_session: AsyncSession):
    account_in = AccountCreate(
        fullname="Test Account", email="test@example.com", password="password123"
    )
    await create_account(async_db_session, account_in)
    account = await authenticate_account(
        async_db_session, "test@example.com", "password123"
    )
    assert account is not None


@pytest.mark.asyncio
async def test_create_session(async_db_session: AsyncSession):
    account_in = AccountCreate(
        fullname="Test Account", email="test@example.com", password="password123"
    )
    account = await create_account(async_db_session, account_in)
    access_token = await create_session(account.id)
    assert access_token is not None
