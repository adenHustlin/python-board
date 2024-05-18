import pytest
from fastapi import status

from app.schemas.board import BoardCreate


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


@pytest.fixture
async def create_board(client, get_token_header):
    async def _create_board():
        headers = await get_token_header()
        board_in = BoardCreate(name="Test Board", public=True)
        response = await client.post(
            "/api/v1/board", json=board_in.dict(), headers=headers
        )
        return response.json(), headers

    return _create_board


@pytest.mark.asyncio
async def test_create_new_post(client, create_board):
    board, headers = await create_board()
    post_in = {
        "board_id": board["id"],
        "title": "Test Post",
        "content": "This is a test post.",
    }
    response = await client.post("/api/v1/post", json=post_in, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == "Test Post"
    assert post["content"] == "This is a test post."
    assert post["owner_id"] == board["owner_id"]


@pytest.mark.asyncio
async def test_read_post(client, create_board):
    board, headers = await create_board()
    post_in = {
        "board_id": board["id"],
        "title": "Test Post",
        "content": "This is a test post.",
    }
    create_post_response = await client.post(
        "/api/v1/post", json=post_in, headers=headers
    )
    post_id = create_post_response.json()["id"]

    response = await client.get(f"/api/v1/post/{post_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == "Test Post"
    assert post["content"] == "This is a test post."
    assert post["owner_id"] == board["owner_id"]


@pytest.mark.asyncio
async def test_update_post(client, create_board):
    board, headers = await create_board()
    post_in = {
        "board_id": board["id"],
        "title": "Test Post",
        "content": "This is a test post.",
    }
    create_post_response = await client.post(
        "/api/v1/post", json=post_in, headers=headers
    )
    post_id = create_post_response.json()["id"]

    post_update = {"title": "Updated Post", "content": "This is an updated test post."}
    response = await client.put(
        f"/api/v1/post/{post_id}", json=post_update, headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == "Updated Post"
    assert post["content"] == "This is an updated test post."
    assert post["owner_id"] == board["owner_id"]


@pytest.mark.asyncio
async def test_delete_post(client, create_board):
    board, headers = await create_board()
    post_in = {
        "board_id": board["id"],
        "title": "Test Post",
        "content": "This is a test post.",
    }
    create_post_response = await client.post(
        "/api/v1/post", json=post_in, headers=headers
    )
    post_id = create_post_response.json()["id"]

    response = await client.delete(f"/api/v1/post/{post_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Post deleted"}

    response = await client.get(f"/api/v1/post/{post_id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_list_posts(client, create_board):
    board, headers = await create_board()

    for i in range(15):
        post_in = {
            "board_id": board["id"],
            "title": f"Test Post {i}",
            "content": "This is a test post.",
        }
        await client.post("/api/v1/post", json=post_in, headers=headers)

    response = await client.get(
        f"/api/v1/posts?board_id={board['id']}&limit=10", headers=headers
    )
    assert response.status_code == status.HTTP_200_OK
    posts = response.json()
    assert posts["total"] == 15
    assert len(posts["posts"]) == 10
    assert posts["next_cursor"] is not None

    response = await client.get(
        f"/api/v1/posts?board_id={board['id']}&limit=10&cursor={posts['next_cursor']}",
        headers=headers,
    )
    assert response.status_code == status.HTTP_200_OK
    posts = response.json()
    assert posts["total"] == 15
    assert len(posts["posts"]) == 5
    assert posts["next_cursor"] is None
