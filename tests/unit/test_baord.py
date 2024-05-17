import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.board import (
    create_board,
    delete_board,
    get_board,
    get_boards,
    update_board,
)
from app.db.models import Account
from app.schemas.board import BoardCreate, BoardUpdate


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


@pytest.mark.asyncio
async def test_get_board(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()
    board_in = BoardCreate(name="Test Board", public=True)
    board = await create_board(async_db_session, board_in, account.id)
    fetched_board = await get_board(async_db_session, board.id)
    assert fetched_board is not None
    assert fetched_board.name == "Test Board"
    assert fetched_board.public is True
    assert fetched_board.owner_id == account.id


@pytest.mark.asyncio
async def test_update_board(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()
    board_in = BoardCreate(name="Test Board", public=True)
    board = await create_board(async_db_session, board_in, account.id)
    board_update = BoardUpdate(name="Updated Board", public=False)
    updated_board = await update_board(
        async_db_session, board_update, board.id, account.id
    )
    assert updated_board.name == "Updated Board"
    assert updated_board.public is False
    assert updated_board.owner_id == account.id


@pytest.mark.asyncio
async def test_delete_board(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()
    board_in = BoardCreate(name="Test Board", public=True)
    board = await create_board(async_db_session, board_in, account.id)
    await delete_board(async_db_session, board.id, account.id)
    fetched_board = await get_board(async_db_session, board.id)
    assert fetched_board is None


@pytest.mark.asyncio
async def test_get_boards(async_db_session: AsyncSession):
    account = Account(
        fullname="Test User", email="testuser@example.com", hashed_password="password"
    )
    async_db_session.add(account)
    await async_db_session.commit()

    for i in range(15):
        board_in = BoardCreate(name=f"Test Board {i}", public=True)
        await create_board(async_db_session, board_in, account.id)

    total, boards, next_cursor = await get_boards(
        async_db_session, account.id, limit=10
    )
    assert total == 15
    assert len(boards) == 10
    assert next_cursor is not None

    total, boards, next_cursor = await get_boards(
        async_db_session, account.id, limit=10, cursor=next_cursor
    )
    assert total == 15
    assert len(boards) == 5
    assert next_cursor is None
