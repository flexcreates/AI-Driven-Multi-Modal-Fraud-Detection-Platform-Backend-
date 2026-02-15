# AI-Driven Multi-Modal Fraud Detection Platform (Backend)

## 📌 Project Overview
Backend system for a comprehensive fraud detection platform. It orchestrates AI model analysis (text, document, image, URL), risk scoring, and real-time alerting to prevent fraud.

**Key Features:**
- **Multi-Modal Analysis**: Text, URL, document, and image analysis endpoints
- **Document Scanning**: Fraud and malware detection in PDF/DOCX files
- **Image Forensics**: Metadata anomalies and steganography detection
- **Risk Scoring**: Configurable weighted scoring engine with ALLOW/FLAG/BLOCK decisions
- **Security**: JWT authentication, role-based access, bcrypt password hashing
- **Logging**: Centralized rotating file logs for all components
- **CORS**: Pre-configured for frontend development servers

## 🛠️ Technology Stack
| Component | Technology |
|-----------|-----------|
| Framework | FastAPI (Python 3.12+, async) |
| Database | PostgreSQL (asyncpg + SQLAlchemy) |
| Auth | JWT (python-jose) + bcrypt |
| Validation | Pydantic V2 |
| Testing | pytest + pytest-asyncio + httpx |

## 📁 Directory Structure
```
BACKEND_API/
├── DATABASE/               # SQL schemas, migrations, seed data
│   ├── schema.sql          # DDL for all 6 tables
│   └── seed_data.sql       # Initial test data
├── SRC/
│   ├── api/
│   │   ├── deps.py         # Auth dependencies (get_current_user)
│   │   ├── docs/auth.py    # Auth endpoints (register, login)
│   │   └── v1/endpoints/
│   │       └── analysis.py # Analysis endpoints (text, url, file, image, history)
│   ├── config/settings.py  # Environment configuration
│   ├── core/security.py    # JWT & password hashing
│   ├── database/           # Async DB session & base model
│   ├── logs/logger.py      # Rotating file logger
│   ├── middleware/          # CORS + request logging
│   ├── models/             # SQLAlchemy ORM models (6)
│   ├── schemas/            # Pydantic request/response models
│   ├── services/           # AI service (mock) + risk engine
│   └── main.py             # FastAPI app entry point
├── tests/                  # Async test suite (14 tests)
├── .env                    # Environment variables (not in git)
├── requirements.txt        # Python dependencies
├── init_db.py              # Database initialization script
├── reset_db.py             # Database reset script (destructive)
├── COMMON_DOCUMENTATION.md # Full API specification for all teams
├── REMAINING.md            # Integration guide for frontend & AI teams
└── CREDITS.md              # Contributors
```

## 🚀 Setup Instructions

### 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Database Configuration
Create a `.env` file in the project root:
```ini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fraud_detection_db
SECRET_KEY=your_secret_key_change_in_production
```

### 3. Initialize Database
```bash
python init_db.py
```
This creates the database, runs `schema.sql` (6 tables), and seeds initial data.

### 4. Run the Server
```bash
uvicorn SRC.main:app --reload
```
- API: `http://localhost:8000`
- Swagger Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔑 API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| `POST` | `/auth/register` | Register new user | ❌ |
| `POST` | `/auth/token` | Login & get JWT | ❌ |
| `POST` | `/analyze/text` | Analyze text for fraud | ✅ |
| `POST` | `/analyze/url` | Analyze URL for phishing | ✅ |
| `POST` | `/analyze/file` | Analyze document (PDF/DOCX) | ✅ |
| `POST` | `/analyze/image` | Analyze image (JPG/PNG/GIF) | ✅ |
| `GET`  | `/analyze/history` | Get user's analysis history | ✅ |
| `GET`  | `/health` | Health check | ❌ |

See [COMMON_DOCUMENTATION.md](COMMON_DOCUMENTATION.md) for complete request/response specifications.

## 🧪 Testing
```bash
PYTHONPATH=. pytest -v
```
**14 tests** covering: registration, login, auth edge cases, all 4 analysis types, history, unauthorized access, invalid tokens, and health check.

## 📦 Database Schema
6 tables: `users`, `api_keys`, `analysis_logs`, `risk_components`, `alerts`, `audit_logs`

See [DATABASE/README.md](DATABASE/README.md) for full schema documentation.

## 👥 Contributors
- **Backend Lead & Database Architect**: Aditya Singh (Flex)
- **Team ID**: MLGUQ04A
