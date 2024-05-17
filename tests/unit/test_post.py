import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.post import create_post
from app.db.models import Account, Board
from app.schemas.post import PostCreate


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
