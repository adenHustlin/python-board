from typing import List, Optional

from pydantic import BaseModel


class BoardCreate(BaseModel):
    name: str
    public: bool


class BoardOut(BaseModel):
    id: int
    name: str
    public: bool
    owner_id: int
    post_count: int  # Include post count

    class Config:
        orm_mode = True


class BoardUpdate(BaseModel):
    name: str
    public: bool


class BoardList(BaseModel):
    boards: List[BoardOut]
    total: int
    next_cursor: Optional[int] = None
