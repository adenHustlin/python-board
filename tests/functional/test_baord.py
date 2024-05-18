import pytest
from fastapi import status


@pytest.fixture
async def get_token_header(client, async_db_session):
    async def _get_token_header():
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
        return {"Authorization": f"Bearer {access_token}"}

    return _get_token_header


@pytest.mark.asyncio
async def test_create_new_board(client, get_token_header):
    headers = await get_token_header()
    board_in = {"name": "Test Board", "public": True}
    response = await client.post("/api/v1/board", json=board_in, headers=headers)
    assert response.status_code == status.HTTP_200_OK

    board = response.json()
    assert board["name"] == "Test Board"
    assert board["public"] is True


@pytest.mark.asyncio
async def test_read_board(client, get_token_header):
    headers = await get_token_header()
    board_in = {"name": "Test Board", "public": True}
    create_response = await client.post("/api/v1/board", json=board_in, headers=headers)
    board_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/board/{board_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK

    board = response.json()
    assert board["name"] == "Test Board"
    assert board["public"] is True


@pytest.mark.asyncio
async def test_update_existing_board(client, get_token_header):
    headers = await get_token_header()
    board_in = {"name": "Test Board", "public": True}
    create_response = await client.post("/api/v1/board", json=board_in, headers=headers)
    board_id = create_response.json()["id"]

    board_update = {"name": "Updated Board", "public": False}
    response = await client.put(
        f"/api/v1/board/{board_id}", json=board_update, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK

    board = response.json()
    assert board["name"] == "Updated Board"
    assert board["public"] is False


@pytest.mark.asyncio
async def test_delete_existing_board(client, get_token_header):
    headers = await get_token_header()
    board_in = {"name": "Test Board", "public": True}
    create_response = await client.post("/api/v1/board", json=board_in, headers=headers)
    board_id = create_response.json()["id"]

    response = await client.delete(f"/api/v1/board/{board_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Board deleted"}


@pytest.mark.asyncio
async def test_list_boards(client, get_token_header):
    headers = await get_token_header()

    for i in range(15):
        board_in = {"name": f"Test Board {i}", "public": True}
        await client.post("/api/v1/board", json=board_in, headers=headers)

    response = await client.get("/api/v1/boards?limit=10", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    boards = response.json()
    assert boards["total"] == 15
    assert len(boards["boards"]) == 10
    assert boards["next_cursor"] is not None

    response = await client.get(
        f"/api/v1/boards?limit=10&cursor={boards['next_cursor']}", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    boards = response.json()
    assert boards["total"] == 15
    assert len(boards["boards"]) == 5
    assert boards["next_cursor"] is None
