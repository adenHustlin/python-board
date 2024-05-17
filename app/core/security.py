from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"
SECRET_KEY = settings.SECRET_KEY


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
