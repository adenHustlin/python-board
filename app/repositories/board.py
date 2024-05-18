from typing import Optional

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Board
from app.schemas.board import BoardCreate, BoardUpdate


class BoardRepository:
    @staticmethod
    async def create_board(db: AsyncSession, board: BoardCreate, user_id: int) -> Board:
        # 시간 복잡도: O(1)
        db_board = Board(name=board.name, public=board.public, owner_id=user_id)
        db.add(db_board)
        await db.commit()
        await db.refresh(db_board)
        return db_board

    @staticmethod
    async def get_board(db: AsyncSession, board_id: int) -> Board:
        # 시간 복잡도: O(1)
        result = await db.execute(select(Board).filter(Board.id == board_id))
        return result.scalars().first()

    @staticmethod
    async def update_board(
        db: AsyncSession, board: BoardUpdate, board_id: int, user_id: int
    ) -> Board:
        # 시간 복잡도: O(1)
        db_board = await BoardRepository.get_board(db, board_id)
        if db_board and db_board.owner_id == user_id:
            db_board.name = board.name
            db_board.public = board.public
            await db.commit()
            await db.refresh(db_board)
        return db_board

    @staticmethod
    async def delete_board(db: AsyncSession, board_id: int, user_id: int):
        # 시간 복잡도: O(1)
        db_board = await BoardRepository.get_board(db, board_id)
        if db_board and db_board.owner_id == user_id:
            await db.delete(db_board)
            await db.commit()

    @staticmethod
    async def increment_post_count(db: AsyncSession, board_id: int):
        # 시간 복잡도: O(1)
        db_board = await BoardRepository.get_board(db, board_id)
        if db_board:
            db_board.post_count += 1
            await db.commit()

    @staticmethod
    async def decrement_post_count(db: AsyncSession, board_id: int):
        # 시간 복잡도: O(1)
        db_board = await BoardRepository.get_board(db, board_id)
        if db_board:
            db_board.post_count -= 1
            await db.commit()

    @staticmethod
    async def get_boards(
        db: AsyncSession,
        user_id: int,
        limit: int = 10,
        cursor: Optional[int] = None,
        offset: int = 0,
        order_by_post_count: bool = False,
    ) -> (int, list[Board], Optional[int]):
        # 시간 복잡도: O(n) 또는 O(log n) (커서를 사용하는 경우)
        # 커서를 사용하지 않는 경우, 전체 결과 집합을 가져오므로 O(n)
        # 커서를 사용하는 경우, 인덱스를 사용하여 부분 결과 집합을 가져오므로 O(log n)
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

        if order_by_post_count:
            query = (
                base_query.order_by(Board.post_count.desc(), Board.id)
                .offset(offset)
                .limit(limit + 1)
            )
        else:
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
