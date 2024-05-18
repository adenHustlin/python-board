from datetime import timedelta

import redis.asyncio as redis
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.repositories.account import AccountRepository
from app.utils.exceptions import raise_unauthorized

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# Redis 클라이언트 초기화
redis_client = redis.from_url(settings.REDIS_URL)


async def authenticate_account(db: AsyncSession, email: str, password: str):
    account = await AccountRepository.get_by_email(db, email)
    if not account or not verify_password(password, account.hashed_password):
        raise_unauthorized("Incorrect email or password", code=4012)
    return account


async def create_session(account_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(account_id)}, expires_delta=access_token_expires
    )
    await redis_client.set(
        f"session:{account_id}",
        access_token,
        ex=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return access_token


async def destroy_session(account_id: int):
    await redis_client.delete(f"session:{account_id}")
