# AI-Driven Multi-Modal Fraud Detection Platform (Backend)

## 📌 Project Overview
This is the backend system for a comprehensive fraud detection platform. It orchestrates AI model analysis (text, document, image, URL), risk scoring, and real-time alerting to prevent fraud.

**Key Features:**
- **Multi-Modal Analysis**: Integrates text, URL, document, and image analysis.
- **Advanced Document Scanning**: Detects fraud and malware in PDF/DOCX files.
- **Image/GIF Forensics**: Analyzes metadata and hidden payloads (steganography).
- **Risk Scoring**: Configurable weighted scoring engine.
- **Explainable AI**: SHAP-based explanation for fraud decisions.
- **Security**: JWT authentication, RBAC, input validation.
- **Alerting**: Real-time webhook notifications.
- **Logging**: Centralized, routed logging for full pipeline visibility.

## 🛠️ Technology Stack
- **Framework**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL (with asyncpg/psycopg2)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (Jose)
- **AI Integration**: HuggingFace, Scikit-learn, XGBoost, Librosa, SHAP
- **Containerization**: Docker (planned)

## 📁 Directory Structure
```
BACKEND_API/
├── DATABASE/           # SQL schemas and seed data
├── SRC/
│   ├── api/            # API route handlers
│   ├── config/         # Configuration settings
│   ├── core/           # Core logic (logging, etc.)
│   ├── database/       # Database connection & session
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic models
│   ├── services/       # Business logic & AI integration
│   ├── utils/          # Utility functions
│   └── main.py         # App entry point
├── venv/               # Python virtual environment
├── requirements.txt    # Dependency list
└── init_db.py          # Database initialization script
```

## 🚀 Setup Instructions

### 1. Environment Setup
The project uses a local virtual environment.
```bash
# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Database Configuration
Ensure PostgreSQL is running and you have created a database (default: `fraud_detection_db`). 
Update `.env` file with your credentials:
```ini
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fraud_detection_db
SECRET_KEY=your_secret_key
```

### 4. Initialize Database
Run the initialization script to create tables and seed data:
```bash
python init_db.py
```
This will:
- Create the `fraud_detection_db` if it doesn't exist.
- Run `DATABASE/schema.sql` to create tables.
- Run `DATABASE/seed_data.sql` to insert initial data.

### 5. Running the Application
Start the development server:
```bash
uvicorn SRC.main:app --reload
```
The API will be available at `http://localhost:8000`.
API Documentation (Swagger UI): `http://localhost:8000/docs`.

## 🧪 Testing
Run health check:
```bash
curl http://localhost:8000/health
```

## 👥 Contributors
- **Backend Lead & Database Architect**: Aditya Singh (Flex)
- **Team ID**: MLGUQ04A
