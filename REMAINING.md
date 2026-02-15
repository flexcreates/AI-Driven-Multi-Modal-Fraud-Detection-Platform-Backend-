# 📋 REMAINING — Integration Guide for Teammates

**Project:** AI-Driven Multi-Modal Fraud Detection Platform  
**Backend Status:** ✅ Complete & Tested (14/14 tests passing)  
**Team ID:** MLGUQ04A

---

## What's Done (Backend — Aditya/Flex)

| Component | Status | Details |
|-----------|--------|---------|
| FastAPI Server | ✅ | Async, fully tested, running on port 8000 |
| PostgreSQL Database | ✅ | 6 tables, ORM models, init/reset scripts |
| Authentication (JWT) | ✅ | Register, login, role-based access |
| Text Analysis API | ✅ | `POST /analyze/text` |
| URL Analysis API | ✅ | `POST /analyze/url` |
| Document Analysis API | ✅ | `POST /analyze/file` (PDF/DOCX) |
| Image Analysis API | ✅ | `POST /analyze/image` (JPG/PNG/GIF) |
| Analysis History API | ✅ | `GET /analyze/history` |
| Risk Engine | ✅ | Score calculation, levels, decisions |
| CORS Middleware | ✅ | Pre-configured for React/Vite dev servers |
| Logging | ✅ | Rotating file logs for all components |

---

## What Remains

### 1. 🎨 Frontend (React) — Frontend Team

The entire user-facing web application needs to be built. The backend is ready to receive requests.

### 2. 🤖 AI Model Server — AI Team

The AI analysis functions are currently **mocked** (returning random scores). They need to be replaced with real trained models.

---

## 🎨 Frontend Integration Guide

### Server Configuration

```
Backend URL:    http://localhost:8000
Swagger Docs:   http://localhost:8000/docs
ReDoc:          http://localhost:8000/redoc
```

CORS is already configured for:
- `http://localhost:3000` (Create React App)
- `http://localhost:5173` (Vite)

If you use a different port, update `SRC/middleware/middleware.py` → `CORS_CONFIG["allow_origins"]`.

---

### Authentication Flow

#### Step 1: Register a User
```
POST http://localhost:8000/auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword123",
    "role": "USER"
}
```

**Response (200):**
```json
{
    "email": "user@example.com",
    "name": "John Doe",
    "is_active": true,
    "role": "USER",
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

#### Step 2: Login & Get Token
```
POST http://localhost:8000/auth/token
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

> **⚠️ IMPORTANT:** The login endpoint uses `username` field (not `email`) and `application/x-www-form-urlencoded` format (not JSON). This is the OAuth2 standard.

**Response (200):**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
}
```

#### Step 3: Use Token for All Protected Endpoints
Store the `access_token` and include it in the `Authorization` header:
```
Authorization: Bearer <access_token>
```

**React example (using axios):**
```javascript
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

// Login
const login = async (email, password) => {
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);

    const res = await axios.post(`${API_BASE}/auth/token`, formData);
    localStorage.setItem('token', res.data.access_token);
    return res.data;
};

// Authenticated API call
const analyzeText = async (content) => {
    const token = localStorage.getItem('token');
    const res = await axios.post(
        `${API_BASE}/analyze/text`,
        { content },
        { headers: { Authorization: `Bearer ${token}` } }
    );
    return res.data;
};
```

---

### Analysis Endpoints (All require JWT)

#### Text Analysis
```
POST /analyze/text
Authorization: Bearer <token>
Content-Type: application/json

{ "content": "Suspicious text to analyze..." }
```

#### URL Analysis
```
POST /analyze/url
Authorization: Bearer <token>
Content-Type: application/json

{ "url": "http://suspicious-url.com" }
```

#### Document Analysis (File Upload)
```
POST /analyze/file
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <PDF or DOCX file>
```

**React file upload example:**
```javascript
const analyzeFile = async (file) => {
    const token = localStorage.getItem('token');
    const formData = new FormData();
    formData.append('file', file);

    const res = await axios.post(`${API_BASE}/analyze/file`, formData, {
        headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
        },
    });
    return res.data;
};
```

#### Image/GIF Analysis (File Upload)
```
POST /analyze/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <JPG, PNG, or GIF file>
```
Works identically to document upload — just use `/analyze/image` instead of `/analyze/file`.

#### Analysis History
```
GET /analyze/history?limit=20
Authorization: Bearer <token>
```

---

### Standard Response Format (All Analysis Endpoints)

```json
{
    "id": "uuid-of-analysis-record",
    "status": "COMPLETED",
    "input_type": "TEXT | URL | DOCUMENT | IMAGE",
    "input_hash": "sha256-hex-digest-64-chars",
    "risk_score": 0.75,
    "risk_level": "LOW | MEDIUM | HIGH",
    "decision": "ALLOW | FLAG | BLOCK",
    "details": {
        "fraud_probability": 0.75,
        "sentiment": "negative",
        "analysis_type": "text"
    },
    "created_at": "2026-02-15T14:30:00+00:00"
}
```

### Error Response Format
```json
{
    "detail": "Error message string"
}
```
Common status codes: `400` (bad request), `401` (unauthorized), `403` (forbidden/inactive), `422` (validation error), `500` (server error).

---

### Frontend Pages to Build

| Page | API Endpoints Used |
|------|-------------------|
| **Login / Register** | `POST /auth/register`, `POST /auth/token` |
| **Dashboard / History** | `GET /analyze/history` |
| **Text Analysis Form** | `POST /analyze/text` |
| **URL Analysis Form** | `POST /analyze/url` |
| **Document Upload** | `POST /analyze/file` |
| **Image/GIF Upload** | `POST /analyze/image` |
| **Health Status** | `GET /health` |

### UI Recommendations
- File uploads: Restrict to `.pdf, .docx, .txt, .jpg, .png, .gif` (max 5MB for MVP)
- Show a loading spinner during analysis (takes ~0.5-1s with mock AI)
- Display risk level with color coding: 🟢 LOW, 🟡 MEDIUM, 🔴 HIGH
- Show decision badges: ✅ ALLOW, ⚠️ FLAG, 🚫 BLOCK

---

## 🤖 AI Service Integration Guide

### Current State
The AI service (`SRC/services/ai_service.py`) contains **4 mock functions** that return random scores. These must be replaced with real model inference.

### Functions to Replace

#### 1. `analyze_text(content: str) -> dict`
**Input:** Raw text string  
**Must return:**
```python
{
    "fraud_probability": 0.85,    # float 0.0-1.0 (REQUIRED)
    "sentiment": "negative",       # str (optional)
    "analysis_type": "text"        # str (keep as "text")
}
```

#### 2. `analyze_url(url: str) -> dict`
**Input:** URL string  
**Must return:**
```python
{
    "phishing_probability": 0.92,  # float 0.0-1.0 (REQUIRED)
    "domain_age": "2 days",        # str (optional)
    "analysis_type": "url"         # str (keep as "url")
}
```

#### 3. `analyze_file(filename: str, file_content: bytes) -> dict`
**Input:** Filename + raw file bytes  
**Must return:**
```python
{
    "malware_probability": 0.78,   # float 0.0-1.0 (REQUIRED)
    "file_type": "pdf",            # str (optional)
    "file_size_bytes": 102400,     # int (optional)
    "analysis_type": "document"    # str (keep as "document")
}
```

#### 4. `analyze_image(filename: str, file_content: bytes) -> dict`
**Input:** Filename + raw image bytes  
**Must return:**
```python
{
    "metadata_suspicion": 0.65,    # float 0.0-1.0 (REQUIRED for risk engine)
    "steganography_score": 0.30,   # float 0.0-1.0 (REQUIRED for risk engine)
    "malware_probability": 0.47,   # float 0.0-1.0 (optional)
    "file_type": "png",            # str (optional)
    "analysis_type": "image"       # str (keep as "image")
}
```

### How to Integrate

**Option A: Direct replacement (same process)**
Replace the mock function bodies with your model inference code directly in `SRC/services/ai_service.py`.

**Option B: Separate AI server (microservice)**
1. Build your AI server (Flask/FastAPI) that exposes endpoints like `/predict/text`, `/predict/url`, etc.
2. Update `SRC/services/ai_service.py` to call your server via HTTP:

```python
import httpx
from SRC.logs.logger import get_logger

logger = get_logger("services.ai")

AI_SERVER_URL = "http://localhost:5000"  # Your AI server

async def analyze_text(content: str) -> dict:
    logger.info(f"Sending text to AI server ({len(content)} chars)")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{AI_SERVER_URL}/predict/text",
            json={"content": content},
            timeout=30.0,
        )
        response.raise_for_status()
        result = response.json()
    logger.info(f"AI response: fraud_probability={result.get('fraud_probability')}")
    return result
```

### Risk Engine Scoring (How Your Scores Are Used)

| Input Type | Key Score Used | Risk Formula |
|------------|---------------|--------------|
| TEXT | `fraud_probability` | Direct use |
| URL | `phishing_probability` | Direct use |
| DOCUMENT/FILE | `malware_probability` | Direct use |
| IMAGE | `metadata_suspicion` + `steganography_score` | `0.6 × metadata + 0.4 × stego` |

**Thresholds:**
- `> 0.8` → **HIGH** → **BLOCK**
- `> 0.4` → **MEDIUM** → **FLAG**
- `≤ 0.4` → **LOW** → **ALLOW**

---

## Environment Setup for All Teams

### Prerequisites
- Python 3.12+
- PostgreSQL (running locally or via Docker)
- Node.js 18+ (Frontend team only)

### Quick Start
```bash
cd BACKEND_API
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fraud_detection_db
SECRET_KEY=your_secret_key_here
EOF

# Initialize database
python init_db.py

# Run server
uvicorn SRC.main:app --reload
# Server at http://localhost:8000, Docs at http://localhost:8000/docs
```
