import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_create_new_board(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    board_in = {"name": "Test Board", "public": True}
    response = await client.post("/api/v1/board", json=board_in, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    account = created_account.json()
    board = response.json()
    assert board["name"] == "Test Board"
    assert board["public"] is True
    assert board["owner_id"] == account["id"]


@pytest.mark.asyncio
async def test_read_board(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    board_in = {"name": "Test Board", "public": True}
    create_response = await client.post("/api/v1/board", json=board_in, headers=headers)
    board_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/board/{board_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    account = created_account.json()
    board = response.json()
    assert board["name"] == "Test Board"
    assert board["public"] is True
    assert board["owner_id"] == account["id"]


@pytest.mark.asyncio
async def test_update_existing_board(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    board_in = {"name": "Test Board", "public": True}
    create_response = await client.post("/api/v1/board", json=board_in, headers=headers)
    board_id = create_response.json()["id"]

    board_update = {"name": "Updated Board", "public": False}
    response = await client.put(
        f"/api/v1/board/{board_id}", json=board_update, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK

    account = created_account.json()
    board = response.json()
    assert board["name"] == "Updated Board"
    assert board["public"] is False
    assert board["owner_id"] == account["id"]


@pytest.mark.asyncio
async def test_delete_existing_board(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    await client.post("/api/v1/signup", json=account_in)
    response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    board_in = {"name": "Test Board", "public": True}
    create_response = await client.post("/api/v1/board", json=board_in, headers=headers)
    board_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/board/{board_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Board deleted"}
