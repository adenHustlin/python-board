import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.board import create_board
from app.db.models import Account
from app.schemas.board import BoardCreate


@pytest.mark.asyncio
async def test_create_board(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()
    board_in = BoardCreate(name="Test Board", public=True)
    board = await create_board(async_db_session, board_in, account.id)
    assert board.name == "Test Board"
    assert board.public is True
    assert board.owner_id == account.id
