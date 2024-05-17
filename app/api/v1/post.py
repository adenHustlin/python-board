from fastapi import APIRouter, Depends, HTTPException
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


from app.crud.post import get_post


@router.get("/post/{post_id}", response_model=PostOut)
async def read_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    db_post = await get_post(db, post_id, current_user.id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
