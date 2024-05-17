from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Board
from app.schemas.board import BoardCreate, BoardUpdate


# Time complexity: O(1) for each database operation
async def create_board(db: AsyncSession, board: BoardCreate, user_id: int) -> Board:
    db_board = Board(name=board.name, public=board.public, owner_id=user_id)
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    return db_board


# Time complexity: O(1) for each database operation
async def get_board(db: AsyncSession, board_id: int) -> Board:
    result = await db.execute(select(Board).filter(Board.id == board_id))
    return result.scalars().first()


# Time complexity: O(1) for each database operation
async def update_board(
    db: AsyncSession, board: BoardUpdate, board_id: int, user_id: int
) -> Board:
    db_board = await get_board(db, board_id)
    if db_board and db_board.owner_id == user_id:
        db_board.name = board.name
        db_board.public = board.public
        await db.commit()
        await db.refresh(db_board)
    return db_board
