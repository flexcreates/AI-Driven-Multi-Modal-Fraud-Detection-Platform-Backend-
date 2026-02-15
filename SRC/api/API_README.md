# Fraud Detection API Documentation

## 🏗️ Architecture

Layered async architecture: FastAPI → Auth → Router → AI Service → Risk Engine → PostgreSQL.

```
Client Request → JWT Validation → Router → AI Service (mock) → Risk Engine → DB → JSON Response
```

## 🚀 Setup & Run

### Prerequisites
- PostgreSQL running (`fraud_detection_db`)
- `.env` file configured (see root README)

### Running
```bash
source venv/bin/activate
uvicorn SRC.main:app --reload
```
Server: `http://localhost:8000` | Docs: `/docs` | ReDoc: `/redoc`

### Testing
```bash
PYTHONPATH=. pytest -v
```

## 📂 API File Structure
```
api/
├── deps.py                     # get_current_user, get_current_active_user
├── docs/
│   └── auth.py                 # POST /auth/register, POST /auth/token
└── v1/endpoints/
    └── analysis.py             # POST /analyze/text|url|file|image, GET /analyze/history
```

## 🔑 Endpoint Reference

| Method | Path | Auth | Content-Type | Description |
|--------|------|------|-------------|-------------|
| `POST` | `/auth/register` | ❌ | `application/json` | Register user |
| `POST` | `/auth/token` | ❌ | `x-www-form-urlencoded` | Login (returns JWT) |
| `POST` | `/analyze/text` | ✅ | `application/json` | Text fraud analysis |
| `POST` | `/analyze/url` | ✅ | `application/json` | URL phishing analysis |
| `POST` | `/analyze/file` | ✅ | `multipart/form-data` | Document analysis |
| `POST` | `/analyze/image` | ✅ | `multipart/form-data` | Image analysis |
| `GET`  | `/analyze/history` | ✅ | — | User's analysis history |
| `GET`  | `/health` | ❌ | — | Health check |

## 🔒 Authentication
1. Register: `POST /auth/register` with JSON body
2. Login: `POST /auth/token` with form data (`username` + `password`)
3. Use token: `Authorization: Bearer <token>` header on all `/analyze/*` endpoints

## 📊 Analysis Response
All analysis endpoints return `AnalysisResponse`:
```json
{
    "id": "uuid",
    "status": "COMPLETED",
    "input_type": "TEXT|URL|DOCUMENT|IMAGE",
    "input_hash": "sha256-64-chars",
    "risk_score": 0.75,
    "risk_level": "LOW|MEDIUM|HIGH",
    "decision": "ALLOW|FLAG|BLOCK",
    "details": { "...ai-specific data..." },
    "created_at": "2026-02-15T14:30:00+00:00"
}
```

For complete API specification with request/response examples, see [COMMON_DOCUMENTATION.md](../../COMMON_DOCUMENTATION.md).
