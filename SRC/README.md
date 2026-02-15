# AI-Driven Multi-Modal Fraud Detection Platform - Backend API

## 📌 Overview
This is the backend API for a professional Fraud Detection Platform. It is built using **FastAPI** and is fully asynchronous, leveraging **PostgreSQL** (via `asyncpg` + `SQLAlchemy`) for high-performance database interactions.

The system provides:
- **User Authentication**: Secure JWT-base login and registration.
- **Risk Analysis**: Evaluates Text, URLs, and Files for fraud risk.
- **Risk Engine**: Calculates risk scores and makes decisions (ALLOW/FLAG/BLOCK).
- **Audit Logging**: Asynchronously logs all analysis requests for compliance.

## 📂 Project Structure

```
SRC/
├── api/            # API Routes (Auth, Analysis)
├── config/         # Environment Configuration
├── core/           # Security (JWT, Hashing)
├── database/       # Async Database Session & Base
├── models/         # SQLAlchemy ORM Models
├── schemas/        # Pydantic Request/Response Models
├── services/       # AI & Risk Logic
└── main.py         # App Entry Point
```

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual Environment

### 2. Environment Setup
Create a `.env` file in the root directory:
```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fraud_detection_db
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Database Setup
The application uses SQLAlchemy for ORM. Tables are created automatically on startup (dev mode) or via migration scripts.
*Note: Ensure your PostgreSQL server is running and the database exists.*

## 🏃 Running the Application
Start the development server with hot-reload:
```bash
uvicorn SRC.main:app --reload
```
The API will be available at: `http://localhost:8000`
Interactive Documentation: `http://localhost:8000/docs`

## 🧪 Testing
The project includes a comprehensive Async Test Suite using `pytest`.
```bash
PYTHONPATH=. pytest
```
Tests cover:
- User Registration & Login
- JWT Token Generation
- Text, URL, and File Analysis flows
- Database Persistence

## 🔑 Key Features
- **Async/Await**: Fully non-blocking I/O for database and generic tasks.
- **Security**: Password hashing with `bcrypt`, JWT for stateless auth.
- **Validation**: Strict data validation using `Pydantic`.
- **Modularity**: Clean architecture separating Routes, Services, and Repositories.

## 📄 API Documentation
For detailed API endpoint usage, see [SRC/api/API_README.md](api/API_README.md).
