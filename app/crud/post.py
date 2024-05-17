from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Board, Post
from app.schemas.post import PostCreate, PostUpdate


# Time complexity: O(1) for each database operation
async def create_post(db: AsyncSession, post: PostCreate, user_id: int) -> Post:

    board = await db.execute(select(Board).filter(Board.id == post.board_id))
    board = board.scalars().first()
    if not board or (not board.public and board.owner_id != user_id):
        raise HTTPException(
            status_code=403, detail="Forbidden: You cannot create a post in this board"
        )

    db_post = Post(
        board_id=post.board_id, title=post.title, content=post.content, owner_id=user_id
    )
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post


# Time complexity: O(1) for each database operation
async def get_post(db: AsyncSession, post_id: int, user_id: int) -> Post:
    query = (
        select(Post)
        .join(Board)
        .filter(Post.id == post_id)
        .filter((Board.public == True) | (Board.owner_id == user_id))
    )
    result = await db.execute(query)
    return result.scalars().first()


# Time complexity: O(1) for each database operation
async def update_post(
    db: AsyncSession, post: PostUpdate, post_id: int, user_id: int
) -> Post:
    db_post = await get_post(db, post_id, user_id)
    if db_post and db_post.owner_id == user_id:
        db_post.title = post.title
        db_post.content = post.content
        await db.commit()
        await db.refresh(db_post)
    return db_post


# Time complexity: O(1) for each database operation
async def delete_post(db: AsyncSession, post_id: int, user_id: int) -> None:
    db_post = await get_post(db, post_id, user_id)
    if db_post and db_post.owner_id == user_id:
        await db.delete(db_post)
        await db.commit()


# Time complexity: O(n) for each database operation
async def get_posts_by_board(
    db: AsyncSession,
    board_id: int,
    user_id: int,
    limit: int = 10,
    cursor: Optional[int] = None,
) -> (int, List[Post], Optional[int]):
    # Check if the board is accessible by the user
    query = select(Board).filter(Board.id == board_id)
    result = await db.execute(query)
    board = result.scalars().first()
    if not board or (not board.public and board.owner_id != user_id):
        raise HTTPException(
            status_code=403, detail="Forbidden: You cannot access this board"
        )

    base_query = select(Post).filter(Post.board_id == board_id)
    if cursor:
        base_query = base_query.filter(Post.id > cursor)

    total_query = select(func.count(Post.id)).filter(Post.board_id == board_id)
    total_result = await db.execute(total_query)
    total = total_result.scalar()

    query = base_query.order_by(Post.id).limit(limit + 1)
    result = await db.execute(query)
    posts = result.scalars().all()

    if len(posts) > limit:
        next_cursor = posts[-2].id
        posts = posts[:-1]
    else:
        next_cursor = None

    return total, posts, next_cursor
