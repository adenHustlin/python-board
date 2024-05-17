from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.account import create_account, get_account_by_email
from app.db.session import get_db
from app.schemas.account import AccountCreate, AccountOut

router = APIRouter()


@router.post("/signup", response_model=AccountOut)
async def signup(account: AccountCreate, db: AsyncSession = Depends(get_db)):
    db_account = await get_account_by_email(db, account.email)
    if db_account:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await create_account(db, account)
