from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Account
from app.db.session import get_db
from app.dependencies import get_current_account
from app.schemas.post import PostCreate, PostList, PostOut, PostUpdate
from app.services.post import (
    create_post_service,
    delete_post_service,
    get_post_service,
    list_posts_service,
    update_post_service,
)

router = APIRouter()


@router.post("/post", response_model=PostOut)
async def create_new_post(
    post: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) = O(1)
    return await create_post_service(post, current_user.id, db)


@router.get("/post/{post_id}", response_model=PostOut)
async def read_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) + O(1) = O(1)
    return await get_post_service(post_id, current_user.id, db)


@router.put("/post/{post_id}", response_model=PostOut)
async def update_existing_post(
    post_id: int,
    post: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) + O(1) = O(1)
    return await update_post_service(post_id, post, current_user.id, db)


@router.delete("/post/{post_id}")
async def delete_existing_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
):
    # 시간 복잡도: O(1) + O(1) + O(1) = O(1)
    await delete_post_service(post_id, current_user.id, db)
    return {"message": "Post deleted"}


@router.get("/posts", response_model=PostList)
async def list_posts(
    board_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Account = Depends(get_current_account),
    limit: int = Query(10, le=100),
    cursor: Optional[int] = Query(None),
):
    # 시간 복잡도: O(log n) (커서를 사용하는 경우)
    total, posts, next_cursor = await list_posts_service(
        board_id, current_user.id, limit, cursor, db
    )
    return {"posts": posts, "total": total, "next_cursor": next_cursor}
