from typing import List, Optional

from pydantic import BaseModel


class PostCreate(BaseModel):
    board_id: int
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str
    content: str


class PostOut(BaseModel):
    id: int
    board_id: int
    title: str
    content: str
    owner_id: int

    class Config:
        orm_mode = True


class PostList(BaseModel):
    posts: List[PostOut]
    total: int
    next_cursor: Optional[int] = None
