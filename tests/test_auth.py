import pytest
from httpx import AsyncClient
import uuid


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test successful user registration."""
    email = f"test_{uuid.uuid4()}@example.com"
    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "name": "Test User",
            "password": "testpassword",
            "role": "USER",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test that registering with an existing email returns 400."""
    email = f"dup_{uuid.uuid4()}@example.com"
    # First registration
    await client.post(
        "/auth/register",
        json={"email": email, "name": "First", "password": "pass", "role": "USER"},
    )
    # Duplicate registration
    response = await client.post(
        "/auth/register",
        json={"email": email, "name": "Second", "password": "pass", "role": "USER"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Test successful login returns a JWT token."""
    email = f"login_{uuid.uuid4()}@example.com"
    await client.post(
        "/auth/register",
        json={"email": email, "name": "Login User", "password": "testpassword", "role": "USER"},
    )
    response = await client.post(
        "/auth/token",
        data={"username": email, "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password returns 401."""
    email = f"wrongpw_{uuid.uuid4()}@example.com"
    await client.post(
        "/auth/register",
        json={"email": email, "name": "Wrong PW", "password": "correctpass", "role": "USER"},
    )
    response = await client.post(
        "/auth/token",
        data={"username": email, "password": "wrongpass"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent email returns 401."""
    response = await client.post(
        "/auth/token",
        data={"username": "nobody@example.com", "password": "anything"},
    )
    assert response.status_code == 401
