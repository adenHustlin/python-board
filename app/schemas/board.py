from pydantic import BaseModel


class BoardCreate(BaseModel):
    name: str
    public: bool


class BoardOut(BaseModel):
    id: int
    name: str
    public: bool
    owner_id: int

    class Config:
        orm_mode = True
