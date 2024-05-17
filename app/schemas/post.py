from pydantic import BaseModel


class PostCreate(BaseModel):
    board_id: int
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
