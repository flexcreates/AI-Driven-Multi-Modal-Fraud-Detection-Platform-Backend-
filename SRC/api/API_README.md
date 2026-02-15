# Fraud Detection API Documentation

## 🏗️ Architecture

The API follows a layered architecture using **FastAPI** (Async) and **PostgreSQL** (via SQLAlchemy + AsyncPG).

### **Flow**
1.  **Client** sends request (Text, URL, File).
2.  **Auth Layer** validates JWT token (`Authorization: Bearer <token>`).
3.  **Router** (`SRC/api/v1/endpoints/`) dispatches request.
4.  **AI Service** (`SRC/services/ai_service.py`) mocks analysis (returns probabilities).
5.  **Risk Engine** (`SRC/services/risk_engine.py`) calculates `Risk Score`, `Level`, and `Decision`.
6.  **Database** saves the `AnalysisRecord` asynchronously.
7.  **Response** returns the JSON result.

## 🚀 Setup & Run

### Prerequisites
- PostgreSQL running (`fraud_detection_db`)
- `.env` file configured

### Installation
```bash
./venv/bin/pip install -r requirements.txt
```

### Running the Server
```bash
./venv/bin/uvicorn SRC.main:app --reload
```
Server will start at `http://localhost:8000`. API Docs at `/docs`.

### Running Tests
```bash
PYTHONPATH=. ./venv/bin/pytest
```

## 📂 Project Structure
- `SRC/api/`: API Routers (Auth, Analysis).
- `SRC/schemas/`: Pydantic Models (Request/Response).
- `SRC/models/`: SQLAlchemy Database Models.
- `SRC/services/`: Business Logic (AI, Risk).
- `SRC/core/`: Security & Config.
- `SRC/database/`: DB Session & Base.

## 🔑 Key Endpoints
| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Register new user |
| `POST` | `/auth/token` | Login & Get JWT |
| `POST` | `/analyze/text` | Analyze text content |
| `POST` | `/analyze/url` | Analyze URL |
| `POST` | `/analyze/file` | Analyze File (PDF/Image) |

## 🛠️ Utilities
- `add_column.py`: Fixes missing `is_active` in `users` table.
- `add_analysis_columns.py`: Fixes missing columns in `analysis_logs`.
