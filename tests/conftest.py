import asyncio

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import get_db
from app.main import app

DATABASE_URL = settings.DATABASE_URL

# Create a new database engine for the tests
engine = create_async_engine(DATABASE_URL, echo=True, future=True)
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Override the get_db dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_db_session():
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            async_session = TestingSessionLocal(bind=connection)

            yield async_session

            await async_session.close()
            await transaction.rollback()
            await connection.close()


@pytest.fixture(scope="function")
async def client(async_db_session):
    async def override_get_db():
        yield async_db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c
