from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.repositories.account import AccountRepository
from app.schemas.account import TokenData
from app.services.auth import oauth2_scheme, redis_client


async def get_current_account(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        account_id: int = int(payload.get("sub"))
        if account_id is None:
            raise credentials_exception
        token_data = TokenData(account_id=account_id)
    except JWTError:
        raise credentials_exception

    # Check Redis for the session
    redis_token = await redis_client.get(f"session:{account_id}")
    if redis_token:
        return await AccountRepository.get_by_id(db, account_id=token_data.account_id)

    # Check the database if Redis session is not found
    account = await AccountRepository.get_by_id(db, account_id=token_data.account_id)
    if account is None:
        raise credentials_exception

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired or invalid"
    )
