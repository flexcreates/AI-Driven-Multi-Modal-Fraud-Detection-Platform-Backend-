# 📘 Common Documentation & Integration Standards
**Project:** AI-Driven Multi-Modal Fraud Detection Platform  
**Authors:** Backend Lead (Aditya/Flex), Frontend Team, AI Team

---

## 1️⃣ Terminology & Domain Language
To ensure consistency across the Backend (FastAPI), Frontend (React), and AI (Model Training), we will use the following standard definitions:

| Term | Definition | Data Type | Range/Values |
|------|------------|-----------|--------------|
| **Risk Score** | The probability that an item is fraudulent. | `Float` | `0.0` (Safe) to `1.0` (Fraud) |
| **Risk Level** | Categorical classification of the score. | `String` | `LOW`, `MEDIUM`, `HIGH` |
| **Decision** | The final action taken by the system. | `String` | `ALLOW`, `FLAG`, `BLOCK` |
| **Input Hash**| Unique fingerprint of text/file input (SHA256). | `String` | 64-char Hex String |
| **Metadata Score** | Risk associated with file metadata (EXIF, Author, etc.). | `Float` | 0.0 - 1.0 |
| **Malware Score** | Probability of file containing virus/exploit. | `Float` | 0.0 - 1.0 |

---

## 2️⃣ Pipeline Integration Flow

### 🔄 Standard Data Flow
1.  **Frontend (React)**: Collects user input (Text, URL, File).
    -   *Action*: Sends HTTP `POST` request to Backend API.
2.  **Backend (FastAPI)**:
    -   Validates input (MIME type, size).
    -   Authenticates Request (JWT).
    -   **Orchestration**: Sends input to the appropriate AI Model / Scanner.
3.  **AI Service**:
    -   Receives raw input / File bytes.
    -   Returns: `fraud_probability`, `malware_detected`, `metadata_suspicion`.
4.  **Risk Engine (Backend)**:
    -   Aggregates model scores.
    -   Applies Logic: `Score = (0.35 * Text) + (0.25 * URL) + (0.2 * Metadata) + (0.2 * Malware)`
    -   Determines `Risk Level` and `Decision`.
5.  **Database**: Logs the analysis, score, and decision.
6.  **Response**: Backend returns JSON to Frontend.

---

## 3️⃣ API Specification (The Contract)

### 🔐 Authentication headers
All protected endpoints must include:
`Authorization: Bearer <access_token>`

### 📨 1. Text Analysis
**Endpoint:** `POST /analyze/text`
**Frontend sends:**
```json
{
  "content": "Subject: URGENT! Verify your account now at http://bit.ly/fake..."
}
```

### 🔗 2. URL Analysis
**Endpoint:** `POST /analyze/url`
**Frontend sends:**
```json
{
  "url": "http://paypal-secure-login.com"
}
```

### 📄 3. Document Analysis (Malware/Fraud)
**Endpoint:** `POST /analyze/document`
**Content-Type:** `multipart/form-data`
**Frontend sends:**
- file: `invoice.pdf`, `contract.docx`, etc.

**Backend returns:**
```json
{
  "risk_score": 0.92,
  "risk_level": "HIGH",
  "decision": "BLOCK",
  "details": {
    "malware_score": 0.9,
    "text_score": 0.4
  }
}
```

### 🖼️ 4. Image/GIF Analysis (Steganography/Metadata)
**Endpoint:** `POST /analyze/image`
**Content-Type:** `multipart/form-data`
**Frontend sends:**
- file: `funny_cat.gif`, `screenshot.jpg`

**Backend checks:**
- **Visuals**: OCR for text in image.
- **Metadata**: EXIF data for anomalies (e.g., location spoofing).
- **Steganography**: Hidden payloads in bits.

---

## 4️⃣ Requirements for AI Team (Model Training)

### **Document Scanner**
-   **Input:** PDF/DOCX bytes.
-   **Tasks:**
    -   Extract Text -> Run *Text Model*.
    -   Scan Structure -> Detect *Malicious Macros/Scripts*.

### **Image/GIF Scanner**
-   **Input:** Image bytes.
-   **Tasks:**
    -   **Metadata Analysis**: Check for manipulation.
    -   **Steganography Detection**: Detect hidden data.
    -   **OCR**: Extract text -> Run *Text Model*.

---

## 5️⃣ Requirements for Frontend Team (React)

1.  **File Uploads**:
    -   Restrict file types: `.pdf, .docx, .txt, .jpg, .png, .gif`.
    -   Max Size: 5MB (for MVP).
2.  **Visuals**:
    -   Show analysis progress (0-100%).
    -   Display "Safe" or "Infected" badges for files.

---

## 6️⃣ Feature Checklist (MVP Phase 1)
- [ ] User Registration & Login (JWT)
- [ ] Dashboard (Recent Activity Logs)
- [ ] Text Analysis Input Form
- [ ] URL Analysis Input Form
- [ ] Document Upload (PDF/DOCX)
- [ ] Image/GIF Upload
- [ ] Malware/Virus Scan Result View
- [ ] Admin View (System-wide Alerts)
