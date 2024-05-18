import pytest
from fastapi import status

from app.schemas.account import AccountCreate


@pytest.fixture
async def create_account(client):
    async def _create_account(email: str, password: str, fullname: str = "Test User"):
        account_in = AccountCreate(fullname=fullname, email=email, password=password)
        response = await client.post("/api/v1/signup", json=account_in.dict())
        assert response.status_code == status.HTTP_200_OK
        return response.json()

    return _create_account


@pytest.fixture
async def login_account(client, create_account):
    async def _login_account(email: str, password: str):
        # 시간 복잡도: O(1)
        await create_account(email=email, password=password)
        response = await client.post(
            "/api/v1/login",
            data={"username": email, "password": password},
        )
        assert response.status_code == status.HTTP_200_OK
        return response.json()

    return _login_account


@pytest.mark.asyncio
async def test_signup(client):
    account_in = AccountCreate(
        fullname="Test Account", email="test@example.com", password="password123"
    )
    response = await client.post("/api/v1/signup", json=account_in.dict())
    assert response.status_code == status.HTTP_200_OK
    account = response.json()
    assert account["email"] == "test@example.com"
    assert account["fullname"] == "Test Account"


@pytest.mark.asyncio
async def test_login(client, login_account):
    token = await login_account(email="testuser@example.com", password="password123")
    assert "access_token" in token
    assert token["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_logout(client, login_account):
    token = await login_account(email="testuser@example.com", password="password123")
    access_token = token["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = await client.post("/api/v1/logout", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Logged out successfully"}
