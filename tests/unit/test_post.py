import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.post import (
    create_post,
    delete_post,
    get_post,
    get_posts_by_board,
    update_post,
)
from app.db.models import Account, Board
from app.schemas.post import PostCreate, PostUpdate


@pytest.mark.asyncio
async def test_create_post(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()

    board = Board(name="Test Board", public=True, owner_id=account.id)
    async_db_session.add(board)
    await async_db_session.commit()

    post_in = PostCreate(
        board_id=board.id, title="Test Post", content="This is a test post."
    )
    post = await create_post(async_db_session, post_in, account.id)
    assert post.title == "Test Post"
    assert post.content == "This is a test post."
    assert post.owner_id == account.id


@pytest.mark.asyncio
async def test_get_post(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()

    board = Board(name="Test Board", public=True, owner_id=account.id)
    async_db_session.add(board)
    await async_db_session.commit()

    post_in = PostCreate(
        board_id=board.id, title="Test Post", content="This is a test post."
    )
    post = await create_post(async_db_session, post_in, account.id)
    fetched_post = await get_post(async_db_session, post.id, account.id)
    assert fetched_post is not None
    assert fetched_post.title == "Test Post"
    assert fetched_post.content == "This is a test post."
    assert fetched_post.owner_id == account.id


@pytest.mark.asyncio
async def test_update_post(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()

    board = Board(name="Test Board", public=True, owner_id=account.id)
    async_db_session.add(board)
    await async_db_session.commit()

    post_in = PostCreate(
        board_id=board.id, title="Test Post", content="This is a test post."
    )
    post = await create_post(async_db_session, post_in, account.id)

    post_update = PostUpdate(
        title="Updated Post", content="This is an updated test post."
    )
    updated_post = await update_post(async_db_session, post_update, post.id, account.id)

    assert updated_post.title == "Updated Post"
    assert updated_post.content == "This is an updated test post."
    assert updated_post.owner_id == account.id


@pytest.mark.asyncio
async def test_delete_post(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()

    board = Board(name="Test Board", public=True, owner_id=account.id)
    async_db_session.add(board)
    await async_db_session.commit()

    post_in = PostCreate(
        board_id=board.id, title="Test Post", content="This is a test post."
    )
    post = await create_post(async_db_session, post_in, account.id)

    await delete_post(async_db_session, post.id, account.id)

    fetched_post = await get_post(async_db_session, post.id, account.id)
    assert fetched_post is None


@pytest.mark.asyncio
async def test_get_posts_by_board(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()

    board = Board(name="Test Board", public=True, owner_id=account.id)
    async_db_session.add(board)
    await async_db_session.commit()

    for i in range(15):
        post_in = PostCreate(
            board_id=board.id, title=f"Test Post {i}", content="This is a test post."
        )
        await create_post(async_db_session, post_in, account.id)

    total, posts, next_cursor = await get_posts_by_board(
        async_db_session, board.id, account.id, limit=10
    )
    assert total == 15
    assert len(posts) == 10
    assert next_cursor is not None

    total, posts, next_cursor = await get_posts_by_board(
        async_db_session, board.id, account.id, limit=10, cursor=next_cursor
    )
    assert total == 15
    assert len(posts) == 5
    assert next_cursor is None
