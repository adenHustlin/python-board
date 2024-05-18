from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.models import Post
from app.repositories.board import BoardRepository
from app.schemas.post import PostCreate, PostUpdate


class PostRepository:
    @staticmethod
    async def create_post(db: AsyncSession, post: PostCreate, user_id: int) -> Post:
        # 시간 복잡도: O(1)
        db_post = Post(
            board_id=post.board_id,
            title=post.title,
            content=post.content,
            owner_id=user_id,
        )
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)

        await BoardRepository.increment_post_count(db, post.board_id)

        return db_post

    @staticmethod
    async def get_post(db: AsyncSession, post_id: int) -> Post:
        # 시간 복잡도: O(1)
        result = await db.execute(select(Post).filter(Post.id == post_id))
        return result.scalars().first()

    @staticmethod
    async def update_post(db: AsyncSession, post: PostUpdate, post_id: int) -> Post:
        # 시간 복잡도: O(1)
        db_post = await PostRepository.get_post(db, post_id)
        if db_post:
            db_post.title = post.title
            db_post.content = post.content
            await db.commit()
            await db.refresh(db_post)
        return db_post

    @staticmethod
    async def delete_post(db: AsyncSession, post_id: int) -> None:
        # 시간 복잡도: O(1)
        db_post = await PostRepository.get_post(db, post_id)
        if db_post:
            board_id = db_post.board_id
            await db.delete(db_post)
            await db.commit()

            await BoardRepository.decrement_post_count(db, board_id)

    @staticmethod
    async def get_posts_by_board(
        db: AsyncSession,
        board_id: int,
        limit: int = 10,
        cursor: Optional[int] = None,
    ) -> (int, List[Post], Optional[int]):
        # 시간 복잡도: O(n) 또는 O(log n) (커서를 사용하는 경우)
        # 커서를 사용하지 않는 경우, 전체 결과 집합을 가져오므로 O(n)
        # 커서를 사용하는 경우, 인덱스를 사용하여 부분 결과 집합을 가져오므로 O(log n)
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
