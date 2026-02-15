import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    email = f"test_{uuid.uuid4()}@example.com"
    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "name": "Test User",
            "password": "testpassword",
            "role": "USER"
        }
    )
    # If user already exists, it might return 400. Handle that.
    if response.status_code == 400:
         assert response.json()["detail"] == "Email already registered"
    else:
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == email
        assert "id" in data

@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    email = f"login_{uuid.uuid4()}@example.com"
    # Ensure user exists
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "name": "Login Test User",
            "password": "testpassword",
            "role": "USER"
        }
    )
    
    response = await client.post(
        "/auth/token",
        data={
            "username": email,
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
