from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Account
from app.db.session import get_db
from app.dependencies import get_current_account
from app.schemas.account import AccountCreate, AccountOut, Token
from app.services.account import signup_service
from app.services.auth import authenticate_account, create_session, destroy_session

router = APIRouter()


@router.post("/signup", response_model=AccountOut)
async def signup(account: AccountCreate, db: AsyncSession = Depends(get_db)):
    # 시간 복잡도: O(1) + O(1) = O(1)
    # 이메일로 계정을 조회하는 작업과 새로운 계정을 생성하는 작업은 모두 시간 복잡도가 O(1)입니다.
    return await signup_service(account, db)


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    # 시간 복잡도: O(1) + O(1) = O(1)
    # 이메일과 비밀번호를 검증하는 작업과 세션을 생성하는 작업은 모두 시간 복잡도가 O(1)입니다.
    account = await authenticate_account(db, form_data.username, form_data.password)
    access_token = await create_session(account.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
async def logout(current_user: Account = Depends(get_current_account)):
    # 시간 복잡도: O(1)
    # 세션을 삭제하는 작업은 시간 복잡도가 O(1)입니다.
    await destroy_session(current_user.id)
    return {"message": "Logged out successfully"}
