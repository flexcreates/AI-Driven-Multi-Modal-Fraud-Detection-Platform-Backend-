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

## 📝 Logging System
The project uses a centralized logging system located in `SRC/logs/logger.py`.
Logs are routed to specific files in `SRC/logs/` based on the component:

- **`backend_main.log`**: General application lifecycle events (Startup/Shutdown).
- **`api.log`**: FastAPI request handling and route-specific logs.
- **`database.log`**: Database connection events and SQL errors.
- **`models.log`**: AI model inference logs (inputs/outputs/errors).

To use the logger in your module:
```python
from SRC.logs.logger import get_logger
logger = get_logger("api.my_module") # Will route to api.log
logger.info("This is an info message")
```

## 🚀 Development
To run the application locally:
```bash
uvicorn SRC.main:app --reload
```

## 🧪 Testing
- **Health Check**: `GET /health` - Verifies API status and DB connection.
