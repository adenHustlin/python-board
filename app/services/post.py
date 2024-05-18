from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.board import BoardRepository
from app.repositories.post import PostRepository
from app.schemas.post import PostCreate, PostUpdate
from app.utils.exceptions import raise_forbidden, raise_not_found


async def create_post_service(post: PostCreate, user_id: int, db: AsyncSession):
    board = await BoardRepository.get_board(db, post.board_id)
    if not board:
        raise_not_found("Board not found", code=4044)
    if not board.public and board.owner_id != user_id:
        raise_forbidden("You cannot create a post in this board", code=4032)
    return await PostRepository.create_post(db, post, user_id)


async def get_post_service(post_id: int, user_id: int, db: AsyncSession):
    db_post = await PostRepository.get_post(db, post_id)
    if not db_post:
        raise_not_found("Post not found", code=4045)
    board = await BoardRepository.get_board(db, db_post.board_id)
    if not board:
        raise_not_found("Board not found", code=4044)
    if not board.public and board.owner_id != user_id:
        raise_forbidden("You do not have permission to access this post", code=4033)
    return db_post


async def update_post_service(
    post_id: int, post: PostUpdate, user_id: int, db: AsyncSession
):
    db_post = await PostRepository.get_post(db, post_id)
    if not db_post:
        raise_not_found("Post not found", code=4045)
    if db_post.owner_id != user_id:
        raise_forbidden("You do not have permission to update this post", code=4034)
    return await PostRepository.update_post(db, post, post_id)


async def delete_post_service(post_id: int, user_id: int, db: AsyncSession):
    db_post = await PostRepository.get_post(db, post_id)
    if not db_post:
        raise_not_found("Post not found", code=4045)
    if db_post.owner_id != user_id:
        raise_forbidden("You do not have permission to delete this post", code=4035)
    await PostRepository.delete_post(db, post_id)


async def list_posts_service(
    board_id: int, user_id: int, limit: int, cursor: Optional[int], db: AsyncSession
):
    board = await BoardRepository.get_board(db, board_id)
    if not board:
        raise_not_found("Board not found", code=4044)
    if not board.public and board.owner_id != user_id:
        raise_forbidden("You do not have permission to access this board", code=4036)
    total, posts, next_cursor = await PostRepository.get_posts_by_board(
        db, board_id, limit, cursor
    )
    return total, posts, next_cursor
