from fastapi import HTTPException
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
