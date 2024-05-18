from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.security import get_password_hash
from app.db.models import Account
from app.schemas.account import AccountCreate


class AccountRepository:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Account:
        # 시간 복잡도: O(1)
        # 데이터베이스 인덱스를 사용하여 이메일로 계정을 조회하므로 시간 복잡도는 O(1)입니다.
        result = await db.execute(select(Account).filter(Account.email == email))
        return result.scalars().first()

    @staticmethod
    async def get_by_id(db: AsyncSession, account_id: int) -> Account:
        # 시간 복잡도: O(1)
        # 데이터베이스 인덱스를 사용하여 ID로 계정을 조회하므로 시간 복잡도는 O(1)입니다.
        result = await db.execute(select(Account).filter(Account.id == account_id))
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, account: AccountCreate) -> Account:
        # 시간 복잡도: O(1)
        # 데이터베이스에 새로운 레코드를 추가하는 작업은 시간 복잡도가 O(1)입니다.
        hashed_password = get_password_hash(account.password)
        db_account = Account(
            email=account.email,
            hashed_password=hashed_password,
            fullname=account.fullname,
        )
        db.add(db_account)
        await db.commit()
        await db.refresh(db_account)
        return db_account
