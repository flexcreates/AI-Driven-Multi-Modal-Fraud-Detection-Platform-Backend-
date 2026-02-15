# Backend API — Source Code Documentation

## 📌 Overview
Fully asynchronous FastAPI backend with PostgreSQL (asyncpg + SQLAlchemy). Provides JWT authentication and multi-modal fraud analysis.

## 📂 Module Breakdown

### `main.py` — Application Entry Point
Initializes the FastAPI app, registers middleware (CORS, request logging), and includes routers.
- **Start:** `uvicorn SRC.main:app --reload`
- **Health:** `GET /health` → `{"status": "UP", "version": "1.0.0"}`

### `api/` — Route Handlers
| File | Endpoints |
|------|-----------|
| `api/deps.py` | `get_current_user`, `get_current_active_user` (auth dependencies) |
| `api/docs/auth.py` | `POST /auth/register`, `POST /auth/token` |
| `api/v1/endpoints/analysis.py` | `POST /analyze/text|url|file|image`, `GET /analyze/history` |

### `config/settings.py` — Configuration
Pydantic `BaseSettings` loading from `.env`: database credentials, JWT secret, token expiry.

### `core/security.py` — Security Utilities
- `create_access_token()` — JWT generation (HS256, 30min default)
- `verify_password()` / `get_password_hash()` — bcrypt hashing

### `database/` — Database Layer
- `base.py` — SQLAlchemy `Base` declarative model
- `session.py` — Async engine, session factory, `get_db()` dependency

### `models/` — SQLAlchemy ORM Models
| Model | Table | Description |
|-------|-------|-------------|
| `User` | `users` | User accounts with roles |
| `AnalysisRecord` | `analysis_logs` | Analysis request records |
| `ApiKey` | `api_keys` | API key management |
| `RiskComponent` | `risk_components` | Breakdown of risk scores |
| `Alert` | `alerts` | Alert/notification records |
| `AuditLog` | `audit_logs` | System audit trail |

### `schemas/` — Pydantic Models
- `user.py` — `UserCreate`, `UserLogin`, `UserResponse`, `Token`
- `analysis.py` — `TextAnalysisRequest`, `UrlAnalysisRequest`, `AnalysisResponse`

### `services/` — Business Logic
- `ai_service.py` — Mock AI analysis functions (text, url, file, image). **Replace with real models.**
- `risk_engine.py` — Calculates risk score, level (LOW/MEDIUM/HIGH), and decision (ALLOW/FLAG/BLOCK).

### `middleware/middleware.py` — Middleware
- `RequestLoggingMiddleware` — Logs method, path, status code, duration for every request
- `CORS_CONFIG` — Pre-configured allowed origins for frontend dev servers

### `logs/logger.py` — Logging System
Rotating file handlers (5MB, 3 backups) routing logs by component:
| Logger Name | Log File |
|------------|----------|
| `api.*` | `api.log` |
| `database.*` | `database.log` |
| `services.*` | `services.log` |
| `middleware.*` | `middleware.log` |
| `main` | `backend_main.log` |

## 🧪 Testing
```bash
PYTHONPATH=. pytest -v
```
14 tests across `test_auth.py`, `test_analysis.py`, and `test_health.py`.
