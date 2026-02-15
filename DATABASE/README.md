# Database Module Documentation

## 📂 Overview
PostgreSQL database for the Fraud Detection Platform. Contains schema definitions, seed data, and migration scripts.

## 📝 Files

### `schema.sql` — Database Schema
Creates 6 tables with constraints and indexes:

| Table | Description | Key Columns |
|-------|-------------|-------------|
| `users` | User accounts | `id`, `email`, `name`, `hashed_password`, `role`, `is_active` |
| `api_keys` | API key management | `user_id`, `api_key`, `status`, `expires_at` |
| `analysis_logs` | Analysis request records | `user_id`, `input_type`, `input_hash`, `risk_score`, `risk_level`, `decision`, `details`, `status` |
| `risk_components` | Risk score breakdown | `analysis_id`, `text_score`, `url_score`, `metadata_score`, `malware_score` |
| `alerts` | Notification records | `analysis_id`, `alert_type`, `sent_to`, `status` |
| `audit_logs` | System audit trail | `user_id`, `action`, `ip_address` |

**Indexes:** `users(email)`, `api_keys(api_key)`, `analysis_logs(user_id)`, `analysis_logs(created_at)`

### `seed_data.sql` — Initial Test Data
Creates 3 default users:
| Email | Role | Password |
|-------|------|----------|
| `admin@fraudplatform.com` | `BANK_ADMIN` | `admin123` |
| `analyst@fraudplatform.com` | `SOC_ANALYST` | `admin123` |
| `client@fraudplatform.com` | `USER` | `admin123` |

Also creates an API key for the client user.

### `migrations/` — Migration Scripts
Reserved directory for future database migrations (currently empty — tables are created via `init_db.py`).

## 🛠️ Usage

### Initialize Database
```bash
python init_db.py
```
Creates the database if it doesn't exist, runs `schema.sql`, then `seed_data.sql`.

### Reset Database (Destructive)
```bash
python reset_db.py           # Interactive confirmation
python reset_db.py --force   # Skip confirmation
```
**⚠️ Warning: This drops and recreates the entire database, deleting all data.**

## 📐 Entity Relationships
```
users ──1:N──▶ analysis_logs
users ──1:N──▶ api_keys
users ──1:N──▶ audit_logs
analysis_logs ──1:N──▶ risk_components
analysis_logs ──1:N──▶ alerts
```
