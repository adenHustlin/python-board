from datetime import timedelta

import redis.asyncio as redis
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.crud.account import get_account_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login")

# Initialize Redis client
redis_client = redis.from_url(settings.REDIS_URL)


# Time complexity: O(1) for each database operation
async def authenticate_account(db: AsyncSession, email: str, password: str):
    account = await get_account_by_email(db, email)
    if not account or not verify_password(password, account.hashed_password):
        return False
    return account


# Time complexity: O(1)
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
