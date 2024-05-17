from typing import Optional

from sqlalchemy import func, select
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


# Time complexity: O(1) for each database operation
async def delete_board(db: AsyncSession, board_id: int, user_id: int):
    db_board = await get_board(db, board_id)
    if db_board and db_board.owner_id == user_id:
        await db.delete(db_board)
        await db.commit()


async def get_boards(
    db: AsyncSession,
    user_id: int,
    limit: int = 10,
    cursor: Optional[int] = None,
    offset: int = 0,
) -> (int, list[Board], Optional[int]):
    base_query = select(Board).filter(
        (Board.owner_id == user_id) | (Board.public == True)
    )

    if cursor:
        base_query = base_query.filter(Board.id > cursor)

    # 전체 게시판 수를 계산하는 쿼리 (커서를 적용하지 않음)
    total_query = select(func.count(Board.id)).filter(
        (Board.owner_id == user_id) | (Board.public == True)
    )

    total_result = await db.execute(total_query)
    total = total_result.scalar()

    query = base_query.order_by(Board.id).offset(offset).limit(limit + 1)
    result = await db.execute(query)
    boards = result.scalars().all()

    if len(boards) > limit:
        next_cursor = boards[
            -2
        ].id  # If there are more records, use the second last ID as next cursor
        boards = boards[:-1]  # Remove the last element
    else:
        next_cursor = None

    return total, boards, next_cursor
