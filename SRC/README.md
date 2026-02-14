# Source Code Documentation (SRC)

## 📂 Structure Overview
The `SRC` directory contains the core application logic for the AI-Driven Multi-Modal Fraud Detection Platform.

```
SRC/
├── api/            # API Endpoints (Routes)
├── config/         # Configuration Settings
├── core/           # Core functionality (Logging, Exceptions)
├── database/       # Database connection & session management
├── models/         # SQLAlchemy ORM Models
├── schemas/        # Pydantic Schemas (Request/Response)
├── services/       # Business Logic & AI Services
├── security/       # Authentication & Authorization
├── middleware/     # Request middleware
├── utils/          # Helper functions
└── main.py         # Application Entry Point
```

## 🔑 Key Components

### 1. Main Application (`main.py`)
- Initializes the FastAPI app.
- Includes API routers.
- Defines the `/health` endpoint for system monitoring.

### 2. Configuration (`config/settings.py`)
- Manages environment variables using `pydantic-settings`.
- Loads sensitive data (DB credentials, Secret Keys) from `.env`.

### 3. Database (`database/session.py`)
- Configures SQLAlchemy engine and session factory.
- Provides `get_db()` dependency for dependency injection in API routes.

## 🚀 Development
To run the application locally:
```bash
uvicorn SRC.main:app --reload
```

## 🧪 Testing
- **Health Check**: `GET /health` - Verifies API status and DB connection.
