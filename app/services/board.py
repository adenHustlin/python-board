from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.board import BoardRepository
from app.schemas.board import BoardCreate, BoardUpdate
from app.utils.exceptions import raise_forbidden, raise_not_found


async def create_board_service(board: BoardCreate, user_id: int, db: AsyncSession):
    return await BoardRepository.create_board(db, board, user_id)


async def get_board_service(board_id: int, user_id: int, db: AsyncSession):
    db_board = await BoardRepository.get_board(db, board_id)
    if not db_board:
        raise_not_found("Board not found", code=4044)
    if not db_board.public and db_board.owner_id != user_id:
        raise_forbidden("You do not have permission to access this board", code=4032)
    return db_board


async def update_board_service(
    board_id: int, board: BoardUpdate, user_id: int, db: AsyncSession
):
    db_board = await BoardRepository.get_board(db, board_id)
    if not db_board:
        raise_not_found("Board not found", code=4044)
    if db_board.owner_id != user_id:
        raise_forbidden("You do not have permission to update this board", code=4033)
    return await BoardRepository.update_board(db, board, board_id, user_id)


async def delete_board_service(board_id: int, user_id: int, db: AsyncSession):
    db_board = await BoardRepository.get_board(db, board_id)
    if not db_board:
        raise_not_found("Board not found", code=4044)
    if db_board.owner_id != user_id:
        raise_forbidden("You do not have permission to delete this board", code=4034)
    await BoardRepository.delete_board(db, board_id, user_id)


async def list_boards_service(
    user_id: int,
    limit: int,
    cursor: Optional[int],
    offset: int,
    db: AsyncSession,
    order_by_post_count: bool,
):
    total, boards, next_cursor = await BoardRepository.get_boards(
        db, user_id, limit, cursor, offset, order_by_post_count
    )
    return total, boards, next_cursor
