import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Account, Board
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate


@pytest.fixture
async def create_test_account(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()
    return account


@pytest.fixture
async def create_test_board(async_db_session: AsyncSession, create_test_account):
    board = Board(name="Test Board", public=True, owner_id=create_test_account.id)
    async_db_session.add(board)
    await async_db_session.commit()
    return board


@pytest.fixture
async def create_test_post(
    async_db_session: AsyncSession, create_test_account, create_test_board
):
    async def _create_test_post(title: str, content: str = "This is a test post."):
        post_in = PostCreate(
            board_id=create_test_board.id, title=title, content=content
        )
        return await PostRepository.create_post(
            async_db_session, post_in, create_test_account.id
        )

    return _create_test_post


@pytest.mark.asyncio
async def test_create_post(
    async_db_session: AsyncSession, create_test_account, create_test_board
):
    post_in = PostCreate(
        board_id=create_test_board.id, title="Test Post", content="This is a test post."
    )
    post = await PostRepository.create_post(
        async_db_session, post_in, create_test_account.id
    )
    assert post.title == "Test Post"
    assert post.content == "This is a test post."
    assert post.owner_id == create_test_account.id


@pytest.mark.asyncio
async def test_get_post(async_db_session: AsyncSession, create_test_post):
    post = await create_test_post(title="Test Post")
    fetched_post = await PostRepository.get_post(async_db_session, post.id)
    assert fetched_post is not None
    assert fetched_post.title == "Test Post"
    assert fetched_post.content == "This is a test post."


@pytest.mark.asyncio
async def test_update_post(async_db_session: AsyncSession, create_test_post):
    post = await create_test_post(title="Test Post")
    post_update = PostUpdate(
        title="Updated Post", content="This is an updated test post."
    )
    updated_post = await PostRepository.update_post(
        async_db_session, post_update, post.id
    )
    assert updated_post.title == "Updated Post"
    assert updated_post.content == "This is an updated test post."


@pytest.mark.asyncio
async def test_delete_post(async_db_session: AsyncSession, create_test_post):
    post = await create_test_post(title="Test Post")
    await PostRepository.delete_post(async_db_session, post.id)
    fetched_post = await PostRepository.get_post(async_db_session, post.id)
    assert fetched_post is None


@pytest.mark.asyncio
async def test_get_posts_by_board(
    async_db_session: AsyncSession, create_test_account, create_test_board
):
    for i in range(15):
        post_in = PostCreate(
            board_id=create_test_board.id,
            title=f"Test Post {i}",
            content="This is a test post.",
        )
        await PostRepository.create_post(
            async_db_session, post_in, create_test_account.id
        )

    total, posts, next_cursor = await PostRepository.get_posts_by_board(
        async_db_session, create_test_board.id, limit=10
    )
    assert total == 15
    assert len(posts) == 10
    assert next_cursor is not None

    total, posts, next_cursor = await PostRepository.get_posts_by_board(
        async_db_session, create_test_board.id, limit=10, cursor=next_cursor
    )
    assert total == 15
    assert len(posts) == 5
    assert next_cursor is None
