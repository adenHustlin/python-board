from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Board
from app.schemas.board import BoardCreate


# Time complexity: O(1) for each database operation
async def create_board(db: AsyncSession, board: BoardCreate, user_id: int) -> Board:
    db_board = Board(name=board.name, public=board.public, owner_id=user_id)
    db.add(db_board)
    await db.commit()
    await db.refresh(db_board)
    return db_board
