import pytest
from httpx import AsyncClient
import uuid
import io


@pytest.mark.asyncio
async def test_text_analysis(client: AsyncClient, auth_headers: dict):
    """Test text analysis endpoint returns a completed analysis record."""
    response = await client.post(
        "/analyze/text",
        json={"content": "Suspicious email content with urgency."},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "TEXT"
    assert data["status"] == "COMPLETED"
    assert "risk_score" in data
    assert "risk_level" in data
    assert "decision" in data
    assert data["input_hash"] is not None
    assert len(data["input_hash"]) == 64  # SHA256 hex digest


@pytest.mark.asyncio
async def test_url_analysis(client: AsyncClient, auth_headers: dict):
    """Test URL analysis endpoint."""
    response = await client.post(
        "/analyze/url",
        json={"url": "http://evil-phishing-site.com"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "URL"
    assert data["status"] == "COMPLETED"
    assert "decision" in data


@pytest.mark.asyncio
async def test_file_analysis(client: AsyncClient, auth_headers: dict):
    """Test file upload analysis endpoint."""
    fake_file = io.BytesIO(b"%PDF-1.4 fake pdf content for testing")
    response = await client.post(
        "/analyze/file",
        files={"file": ("test_invoice.pdf", fake_file, "application/pdf")},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "DOCUMENT"
    assert data["status"] == "COMPLETED"


@pytest.mark.asyncio
async def test_image_analysis(client: AsyncClient, auth_headers: dict):
    """Test image upload analysis endpoint."""
    fake_image = io.BytesIO(b"\x89PNG\r\n\x1a\n fake image content")
    response = await client.post(
        "/analyze/image",
        files={"file": ("suspicious.png", fake_image, "image/png")},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["input_type"] == "IMAGE"
    assert data["status"] == "COMPLETED"
    assert "risk_score" in data


@pytest.mark.asyncio
async def test_analysis_history(client: AsyncClient, auth_headers: dict):
    """Test analysis history retrieval after performing analyses."""
    # Perform a text analysis first
    await client.post(
        "/analyze/text",
        json={"content": "history test content"},
        headers=auth_headers,
    )
    # Fetch history
    response = await client.get(
        "/analyze/history",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert data[0]["input_type"] == "TEXT"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test that analysis endpoints reject unauthenticated requests."""
    response = await client.post(
        "/analyze/text",
        json={"content": "Should be rejected"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_unauthorized_history(client: AsyncClient):
    """Test that history endpoint rejects unauthenticated requests."""
    response = await client.get("/analyze/history")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient):
    """Test that an invalid token is rejected."""
    response = await client.post(
        "/analyze/text",
        json={"content": "Should fail"},
        headers={"Authorization": "Bearer invalidtoken123"},
    )
    assert response.status_code == 401
