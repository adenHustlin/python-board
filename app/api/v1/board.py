from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.board import (
    create_board,
    delete_board,
    get_board,
    get_boards,
    update_board,
)
from app.db.models import Account
from app.db.session import get_db
from app.dependencies import get_current_account
from app.schemas.board import BoardCreate, BoardList, BoardOut, BoardUpdate

router = APIRouter()


@router.post("/board", response_model=BoardOut)
async def create_new_board(
    board: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    new_board = await create_board(db, board, current_user.id)
    return new_board


@router.get("/board/{board_id}", response_model=BoardOut)
async def read_board(
    board_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    db_board = await get_board(db, board_id)
    if not db_board or (not db_board.public and db_board.owner_id != current_user.id):
        raise HTTPException(status_code=404, detail="Board not found")
    return db_board


@router.put("/board/{board_id}", response_model=BoardOut)
async def update_existing_board(
    board_id: int,
    board: BoardUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    updated_board = await update_board(db, board, board_id, current_user.id)
    if not updated_board:
        raise HTTPException(status_code=404, detail="Board not found or not permitted")
    return updated_board


@router.delete("/board/{board_id}")
async def delete_existing_board(
    board_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    await delete_board(db, board_id, current_user.id)
    return {"message": "Board deleted"}


@router.get("/boards", response_model=BoardList)
async def list_boards(
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
    limit: int = Query(10, le=100),
    cursor: Optional[int] = Query(None),
    offset: int = Query(0, ge=0),
):
    total, boards, next_cursor = await get_boards(
        db, current_user.id, limit=limit, cursor=cursor, offset=offset
    )
    return {"boards": boards, "total": total, "next_cursor": next_cursor}
