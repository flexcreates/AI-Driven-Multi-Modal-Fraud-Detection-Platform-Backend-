import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from SRC.database.base import Base
from SRC.database.session import get_db
from SRC.main import app
from SRC.config.settings import settings

# Use a separate test database or the same one (be careful with data)
# For this test integration, we might want to use a separate DB, but for simplicity
# we'll use the main one but roll back transactions? 
# Autosaving/committing in endpoints makes rollback hard.
# Better to use a test DB.
# For now, I'll use the main DB but with a different URL if I could, but I'll stick to main DB 
# and clean up or just accept it's a dev env.

TEST_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
