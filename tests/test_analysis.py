import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_text_analysis(client: AsyncClient):
    email = f"analyst_{uuid.uuid4()}@example.com"
    # Register and Login to get token
    await client.post(
        "/auth/register",
        json={"email": email, "name": "Analyst", "password": "pass", "role": "USER"}
    )
    login_res = await client.post(
        "/auth/token",
        data={"username": email, "password": "pass"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.post(
        "/analyze/text",
        json={"content": "Suspicious email content with urgency."},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "TEXT"
    assert "risk_score" in data
    assert data["status"] == "COMPLETED"

@pytest.mark.asyncio
async def test_url_analysis(client: AsyncClient):
    email = f"url_analyst_{uuid.uuid4()}@example.com"
    # Register and Login
    await client.post(
        "/auth/register",
        json={"email": email, "name": "URL Analyst", "password": "pass", "role": "USER"}
    )
    login_res = await client.post(
        "/auth/token",
        data={"username": email, "password": "pass"}
    )
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.post(
        "/analyze/url",
        json={"url": "http://evil.com"},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "URL"
    assert "decision" in data

# File test skipped for brevity but can be added
