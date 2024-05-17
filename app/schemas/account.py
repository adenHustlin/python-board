from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class AccountOut(BaseModel):
    id: int
    fullname: str
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    account_id: int | None = None
