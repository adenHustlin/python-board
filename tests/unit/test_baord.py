import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Account
from app.repositories.board import BoardRepository
from app.schemas.board import BoardCreate, BoardUpdate


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
    async def _create_test_board(name: str, public: bool = True):
        board_in = BoardCreate(name=name, public=public)
        return await BoardRepository.create_board(
            async_db_session, board_in, create_test_account.id
        )

    return _create_test_board


@pytest.mark.asyncio
async def test_create_board(async_db_session: AsyncSession, create_test_account):
    board_in = BoardCreate(name="Test Board", public=True)
    board = await BoardRepository.create_board(
        async_db_session, board_in, create_test_account.id
    )
    assert board.name == "Test Board"
    assert board.public is True
    assert board.owner_id == create_test_account.id


@pytest.mark.asyncio
async def test_get_board(async_db_session: AsyncSession, create_test_board):
    board = await create_test_board(name="Test Board")
    fetched_board = await BoardRepository.get_board(async_db_session, board.id)
    assert fetched_board is not None
    assert fetched_board.name == "Test Board"
    assert fetched_board.public is True
    assert fetched_board.owner_id == board.owner_id


@pytest.mark.asyncio
async def test_update_board(async_db_session: AsyncSession, create_test_board):
    board = await create_test_board(name="Test Board")
    board_update = BoardUpdate(name="Updated Board", public=False)
    updated_board = await BoardRepository.update_board(
        async_db_session, board_update, board.id, board.owner_id
    )
    assert updated_board.name == "Updated Board"
    assert updated_board.public is False
    assert updated_board.owner_id == board.owner_id


@pytest.mark.asyncio
async def test_delete_board(async_db_session: AsyncSession, create_test_board):
    board = await create_test_board(name="Test Board")
    await BoardRepository.delete_board(async_db_session, board.id, board.owner_id)
    fetched_board = await BoardRepository.get_board(async_db_session, board.id)
    assert fetched_board is None


@pytest.mark.asyncio
async def test_get_boards(async_db_session: AsyncSession, create_test_account):
    for i in range(15):
        board_in = BoardCreate(name=f"Test Board {i}", public=True)
        await BoardRepository.create_board(
            async_db_session, board_in, create_test_account.id
        )

    total, boards, next_cursor = await BoardRepository.get_boards(
        async_db_session, create_test_account.id, limit=10
    )
    assert total == 15
    assert len(boards) == 10
    assert next_cursor is not None

    total, boards, next_cursor = await BoardRepository.get_boards(
        async_db_session, create_test_account.id, limit=10, cursor=next_cursor
    )
    assert total == 15
    assert len(boards) == 5
    assert next_cursor is None
