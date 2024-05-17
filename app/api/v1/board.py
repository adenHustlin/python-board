from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.board import create_board
from app.db.models import Account
from app.db.session import get_db
from app.dependencies import get_current_account
from app.schemas.board import BoardCreate, BoardOut

router = APIRouter()


@router.post("/board", response_model=BoardOut)
async def create_new_board(
    board: BoardCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    new_board = await create_board(db, board, current_user.id)
    return new_board
