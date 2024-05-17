import pytest


@pytest.mark.asyncio
async def test_create_new_post(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    login_response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    board_in = {"name": "Test Board", "public": True}
    create_board_response = await client.post(
        "/api/v1/board", json=board_in, headers=headers
    )
    board_id = create_board_response.json()["id"]

    post_in = {
        "board_id": board_id,
        "title": "Test Post",
        "content": "This is a test post.",
    }
    response = await client.post("/api/v1/post", json=post_in, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["title"] == "Test Post"
    assert post["content"] == "This is a test post."
    assert post["owner_id"] == created_account.json()["id"]


import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_read_post(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    login_response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    board_in = {"name": "Test Board", "public": True}
    create_board_response = await client.post(
        "/api/v1/board", json=board_in, headers=headers
    )
    board_id = create_board_response.json()["id"]

    post_in = {
        "board_id": board_id,
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
    assert post["owner_id"] == created_account.json()["id"]


@pytest.mark.asyncio
async def test_update_post(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    login_response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    board_in = {"name": "Test Board", "public": True}
    create_board_response = await client.post(
        "/api/v1/board", json=board_in, headers=headers
    )
    board_id = create_board_response.json()["id"]

    post_in = {
        "board_id": board_id,
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
    assert post["owner_id"] == created_account.json()["id"]


@pytest.mark.asyncio
async def test_delete_post(client, async_db_session):
    account_in = {
        "fullname": "Test User",
        "email": "testuser@example.com",
        "password": "password123",
    }
    created_account = await client.post("/api/v1/signup", json=account_in)
    login_response = await client.post(
        "/api/v1/login",
        data={"username": "testuser@example.com", "password": "password123"},
    )
    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}

    board_in = {"name": "Test Board", "public": True}
    create_board_response = await client.post(
        "/api/v1/board", json=board_in, headers=headers
    )
    board_id = create_board_response.json()["id"]

    post_in = {
        "board_id": board_id,
        "title": "Test Post",
        "content": "This is a test post.",
    }
    create_post_response = await client.post(
        "/api/v1/post", json=post_in, headers=headers
    )
    post_id = create_post_response.json()["id"]

    response = await client.delete(f"/api/v1/post/{post_id}", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Post deleted successfully"}

    response = await client.get(f"/api/v1/post/{post_id}", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
