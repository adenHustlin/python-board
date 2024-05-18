from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.account import AccountRepository
from app.schemas.account import AccountCreate
from app.utils.exceptions import raise_bad_request, raise_not_found


async def signup_service(account: AccountCreate, db: AsyncSession):
    db_account = await AccountRepository.get_by_email(db, account.email)
    if db_account:
        raise_bad_request("Email already registered", code=4002)
    return await AccountRepository.create(db, account)


async def get_account_service(
    db: AsyncSession,
    email: str = None,
    account_id: int = None,
):
    if email:
        db_account = await AccountRepository.get_by_email(db, email)
        if not db_account:
            raise_not_found("Account not found", code=4042)
        return db_account
    elif account_id:
        db_account = await AccountRepository.get_by_id(db, account_id)
        if not db_account:
            raise_not_found("Account not found", code=4043)
        return db_account
