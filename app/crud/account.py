from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.db.models import Account
from app.schemas.account import AccountCreate


# Time complexity: O(1) for each database operation
async def get_account_by_email(db: AsyncSession, email: str) -> Account:
    result = await db.execute(select(Account).filter(Account.email == email))
    return result.scalars().first()


# Time complexity: O(1) for each database operation
async def get_account_by_id(db: AsyncSession, account_id: int) -> Account:
    result = await db.execute(select(Account).filter(Account.id == account_id))
    return result.scalars().first()


# Time complexity: O(1) for each database operation
async def create_account(db: AsyncSession, account: AccountCreate) -> Account:
    hashed_password = get_password_hash(account.password)
    db_account = Account(
        email=account.email, hashed_password=hashed_password, fullname=account.fullname
    )
    db.add(db_account)
    await db.commit()
    await db.refresh(db_account)
    return db_account
