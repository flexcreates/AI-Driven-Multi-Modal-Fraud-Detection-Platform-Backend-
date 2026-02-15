# 📘 Common Documentation & Integration Standards
**Project:** AI-Driven Multi-Modal Fraud Detection Platform  
**Authors:** Backend Lead (Aditya/Flex), Frontend Team, AI Team  
**Team ID:** MLGUQ04A

---

## 1️⃣ Terminology & Domain Language

| Term | Definition | Data Type | Range/Values |
|------|-----------|-----------|--------------|
| **Risk Score** | Probability that an item is fraudulent | `Float` | `0.0` (Safe) to `1.0` (Fraud) |
| **Risk Level** | Categorical classification of the score | `String` | `LOW`, `MEDIUM`, `HIGH` |
| **Decision** | Final action taken by the system | `String` | `ALLOW`, `FLAG`, `BLOCK` |
| **Input Hash** | SHA256 fingerprint of text/file input | `String` | 64-char hex string |
| **Metadata Score** | Risk from file metadata (EXIF, Author) | `Float` | 0.0 - 1.0 |
| **Malware Score** | Probability of file containing exploit | `Float` | 0.0 - 1.0 |
| **Steganography Score** | Probability of hidden data in image | `Float` | 0.0 - 1.0 |

---

## 2️⃣ Pipeline Integration Flow

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────┐
│   Frontend   │────▶│  Backend (FastAPI)│────▶│  AI Service  │
│   (React)    │     │   Port: 8000     │     │  (Mock/Real) │
└──────────────┘     └────────┬─────────┘     └──────┬───────┘
                              │                       │
                              │◀──────────────────────┘
                              ▼
                     ┌──────────────────┐
                     │   Risk Engine    │
                     │ Score → Decision │
                     └────────┬─────────┘
                              ▼
                     ┌──────────────────┐
                     │   PostgreSQL DB  │
                     │  (analysis_logs) │
                     └──────────────────┘
```

### Data Flow Steps
1. **Frontend**: Sends HTTP request with input (text, URL, or file)
2. **Backend Auth**: Validates JWT token from `Authorization: Bearer <token>` header
3. **Backend Router**: Dispatches to appropriate analysis endpoint
4. **AI Service**: Processes input, returns probability scores
5. **Risk Engine**: Calculates final risk score, level, and decision
6. **Database**: Logs the analysis record to `analysis_logs` table
7. **Response**: Returns JSON result to frontend

---

## 3️⃣ Server Configuration

| Item | Value |
|------|-------|
| **Base URL** | `http://localhost:8000` |
| **API Docs (Swagger)** | `http://localhost:8000/docs` |
| **API Docs (ReDoc)** | `http://localhost:8000/redoc` |
| **Health Check** | `GET http://localhost:8000/health` |

---

## 4️⃣ Complete API Specification

### 🔐 Authentication

#### `POST /auth/register` — Register New User
**Content-Type:** `application/json`  
**Auth Required:** ❌ No

**Request Body:**
```json
{
    "email": "user@example.com",
    "name": "John Doe",
    "password": "securepassword123",
    "role": "USER"
}
```

| Field | Type | Required | Values |
|-------|------|----------|--------|
| `email` | string (email) | ✅ | Valid email address |
| `name` | string | ✅ | User's display name |
| `password` | string | ✅ | Plain text (hashed server-side) |
| `role` | string | ❌ | `USER` (default), `BANK_ADMIN`, `SOC_ANALYST` |

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

**Error (400):** `{"detail": "Email already registered"}`

---

#### `POST /auth/token` — Login & Get JWT
**Content-Type:** `application/x-www-form-urlencoded`  
**Auth Required:** ❌ No

**Request Body (form data, NOT JSON):**
```
username=user@example.com&password=securepassword123
```

| Field | Type | Required | Note |
|-------|------|----------|------|
| `username` | string | ✅ | **This is the email** (OAuth2 standard uses `username`) |
| `password` | string | ✅ | Plain text password |

**Response (200):**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

**Error (401):** `{"detail": "Incorrect username or password"}`

**Token expiry:** 30 minutes (configurable via `ACCESS_TOKEN_EXPIRE_MINUTES` in `.env`)

---

### 📊 Analysis Endpoints (All Require JWT)

All analysis endpoints require:
```
Authorization: Bearer <access_token>
```

#### `POST /analyze/text` — Text Fraud Analysis
**Content-Type:** `application/json`

**Request:**
```json
{
    "content": "URGENT! Your account has been compromised. Click here: http://bit.ly/fake"
}
```

| Field | Type | Required |
|-------|------|----------|
| `content` | string | ✅ |

---

#### `POST /analyze/url` — URL Phishing Analysis
**Content-Type:** `application/json`

**Request:**
```json
{
    "url": "http://paypal-secure-login.com"
}
```

| Field | Type | Required |
|-------|------|----------|
| `url` | string | ✅ |

---

#### `POST /analyze/file` — Document Analysis (Malware/Fraud)
**Content-Type:** `multipart/form-data`

**Request:** Upload file with field name `file`
- Supported: `.pdf`, `.docx`, `.txt`
- Max size: 5MB (recommended for MVP)

---

#### `POST /analyze/image` — Image/GIF Analysis (Steganography/Metadata)
**Content-Type:** `multipart/form-data`

**Request:** Upload file with field name `file`
- Supported: `.jpg`, `.png`, `.gif`
- Checks: Metadata anomalies, steganography, OCR text extraction

---

#### `GET /analyze/history` — Get Analysis History
**Query Parameters:**

| Param | Type | Default | Max |
|-------|------|---------|-----|
| `limit` | int | 20 | 100 |

Returns the authenticated user's analysis records, most recent first.

---

### 📦 Standard Analysis Response (All Analysis Endpoints)

```json
{
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "status": "COMPLETED",
    "input_type": "TEXT",
    "input_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "risk_score": 0.75,
    "risk_level": "MEDIUM",
    "decision": "FLAG",
    "details": {
        "fraud_probability": 0.75,
        "sentiment": "negative",
        "analysis_type": "text"
    },
    "created_at": "2026-02-15T14:30:00+00:00"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `id` | UUID | Unique record identifier |
| `status` | string | `PENDING`, `COMPLETED`, or `FAILED` |
| `input_type` | string | `TEXT`, `URL`, `DOCUMENT`, or `IMAGE` |
| `input_hash` | string | SHA256 hex digest (64 chars) |
| `risk_score` | float | 0.0 (safe) to 1.0 (fraud) |
| `risk_level` | string | `LOW` (≤0.4), `MEDIUM` (0.4-0.8), `HIGH` (>0.8) |
| `decision` | string | `ALLOW`, `FLAG`, or `BLOCK` |
| `details` | object | AI-specific analysis details |
| `created_at` | datetime | ISO 8601 timestamp |

---

### ⚠️ Error Response Format

All errors return:
```json
{
    "detail": "Human-readable error message"
}
```

| Status Code | Meaning |
|-------------|---------|
| `400` | Bad request / validation error |
| `401` | Unauthorized (missing or invalid token) |
| `403` | Forbidden (inactive account) |
| `422` | Unprocessable entity (invalid input format) |
| `500` | Internal server error |

---

### 🏥 System

#### `GET /health` — Health Check
**Auth Required:** ❌ No

**Response (200):**
```json
{
    "status": "UP",
    "version": "1.0.0"
}
```

---

## 5️⃣ Risk Engine Scoring Logic

```
Score = AI probability score (0.0 — 1.0)

TEXT:     score = fraud_probability
URL:      score = phishing_probability
DOCUMENT: score = malware_probability
IMAGE:    score = (0.6 × metadata_suspicion) + (0.4 × steganography_score)
```

| Score Range | Risk Level | Decision |
|-------------|-----------|----------|
| > 0.8 | **HIGH** 🔴 | **BLOCK** |
| > 0.4 | **MEDIUM** 🟡 | **FLAG** |
| ≤ 0.4 | **LOW** 🟢 | **ALLOW** |

---

## 6️⃣ Requirements for AI Team (Model Training)

### Text Model
- **Input:** Raw text string
- **Output:** `fraud_probability` (float 0.0-1.0)
- **Approach:** NLP classification (phishing, scam, spam detection)

### URL Model
- **Input:** URL string
- **Output:** `phishing_probability` (float 0.0-1.0)
- **Approach:** Domain analysis, content inspection, URL pattern matching

### Document Scanner
- **Input:** PDF/DOCX file bytes
- **Output:** `malware_probability` (float 0.0-1.0)
- **Tasks:** Text extraction → text model, structure scan → malicious macro detection

### Image Scanner
- **Input:** Image file bytes
- **Output:** `metadata_suspicion` + `steganography_score` (float 0.0-1.0 each)
- **Tasks:** EXIF analysis, steganography detection, OCR → text model

---

## 7️⃣ Requirements for Frontend Team (React)

### File Upload Constraints
- Allowed types: `.pdf, .docx, .txt, .jpg, .png, .gif`
- Max file size: 5MB (MVP)

### Recommended UI Components
1. **Login/Register** form
2. **Analysis Dashboard** with recent history (from `GET /analyze/history`)
3. **Text Analysis** — text input form
4. **URL Analysis** — URL input form
5. **File Upload** — drag-and-drop with type validation
6. **Results Display** — risk score gauge, level badge, decision indicator

### Visual Guidelines
- Risk levels: 🟢 LOW (green), 🟡 MEDIUM (yellow/amber), 🔴 HIGH (red)
- Decisions: ✅ ALLOW, ⚠️ FLAG, 🚫 BLOCK
- Show loading/progress during analysis

---

## 8️⃣ Feature Checklist (MVP Phase 1)
- [x] User Registration & Login (JWT) — **Backend Done**
- [x] Text Analysis API — **Backend Done**
- [x] URL Analysis API — **Backend Done**
- [x] Document Upload Analysis — **Backend Done**
- [x] Image/GIF Upload Analysis — **Backend Done**
- [x] Analysis History — **Backend Done**
- [ ] Frontend Dashboard (React) — **Frontend Team**
- [ ] AI Model Integration — **AI Team**
- [ ] Admin View (System-wide Alerts) — **Phase 2**
