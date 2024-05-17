from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.post import create_post
from app.db.models import Account
from app.db.session import get_db
from app.dependencies import get_current_account
from app.schemas.post import PostCreate, PostOut

router = APIRouter()


@router.post("/post", response_model=PostOut)
async def create_new_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    new_post = await create_post(db, post, current_user.id)
    return new_post
