from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Account
from app.db.session import get_db
from app.dependencies import get_current_account
from app.schemas.board import BoardCreate, BoardList, BoardOut, BoardUpdate
from app.services.board import (
    create_board_service,
    delete_board_service,
    get_board_service,
    list_boards_service,
    update_board_service,
)

router = APIRouter()


@router.post("/board", response_model=BoardOut)
async def create_new_board(
    board: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1)
    return await create_board_service(board, current_user.id, db)


@router.get("/board/{board_id}", response_model=BoardOut)
async def read_board(
    board_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) + O(1) = O(1)
    return await get_board_service(board_id, current_user.id, db)


@router.put("/board/{board_id}", response_model=BoardOut)
async def update_existing_board(
    board_id: int,
    board: BoardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) = O(1)
    return await update_board_service(board_id, board, current_user.id, db)


@router.delete("/board/{board_id}")
async def delete_existing_board(
    board_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) = O(1)
    await delete_board_service(board_id, current_user.id, db)
    return {"message": "Board deleted"}


@router.get("/boards", response_model=BoardList)
async def list_boards(
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
    limit: int = Query(10, le=100),
    cursor: Optional[int] = Query(None),
    offset: int = Query(0, ge=0),
    order_by_post_count: bool = Query(False),
):
    # 시간 복잡도: O(n) 또는 O(log n) (커서를 사용하는 경우)
    total, boards, next_cursor = await list_boards_service(
        current_user.id, limit, cursor, offset, db, order_by_post_count
    )
    return {"boards": boards, "total": total, "next_cursor": next_cursor}
