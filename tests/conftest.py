import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import uuid

from SRC.database.base import Base
from SRC.database.session import get_db
from SRC.main import app
from SRC.config.settings import settings

# Use the same database for testing (dev environment)
TEST_DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Import all models to ensure they are registered with Base.metadata
from SRC.models.user import User
from SRC.models.analysis import AnalysisRecord
from SRC.models.api_key import ApiKey
from SRC.models.risk_component import RiskComponent
from SRC.models.alert import Alert
from SRC.models.audit_log import AuditLog


@pytest.fixture(autouse=True)
async def setup_db():
    """Create all tables before each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session for tests."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide an async HTTP test client with DB override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
async def auth_headers(client: AsyncClient) -> dict:
    """Register a test user and return auth headers with a valid JWT token."""
    email = f"fixture_{uuid.uuid4()}@test.com"
    await client.post(
        "/auth/register",
        json={"email": email, "name": "Test Fixture User", "password": "testpass123", "role": "USER"},
    )
    login_res = await client.post(
        "/auth/token",
        data={"username": email, "password": "testpass123"},
    )
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
