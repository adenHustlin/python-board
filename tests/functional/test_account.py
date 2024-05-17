import pytest
from fastapi import status

from app.schemas.account import AccountCreate


@pytest.mark.asyncio
async def test_signup(client, async_db_session):
    account_in = AccountCreate(
        fullname="Test Account", email="test@example.com", password="password123"
    )
    response = await client.post("/api/v1/signup", json=account_in.dict())
    assert response.status_code == status.HTTP_200_OK
    account = response.json()
    assert account["email"] == "test@example.com"
    assert account["fullname"] == "Test Account"


@pytest.mark.asyncio
async def test_login(client, async_db_session):
    account_in = AccountCreate(
        fullname="Test User", email="testuser@example.com", password="password123"
    )
    await client.post("/api/v1/signup", json=account_in.dict())
    response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    assert response.status_code == status.HTTP_200_OK
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"
