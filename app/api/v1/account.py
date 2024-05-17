from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.account import create_account, get_account_by_email
from app.db.session import get_db
from app.schemas.account import AccountCreate, AccountOut, Token
from app.services.auth import authenticate_account, create_session

router = APIRouter()


@router.post("/signup", response_model=AccountOut)
async def signup(account: AccountCreate, db: AsyncSession = Depends(get_db)):
    db_account = await get_account_by_email(db, account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_account(db, account)


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    account = await authenticate_account(db, form_data.username, form_data.password)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_session(account.id)
    return {"access_token": access_token, "token_type": "bearer"}
