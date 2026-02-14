# Database Module Documentation

## 📂 Overview
The `DATABASE` directory contains all SQL scripts and migration files necessary for setting up and managing the PostgreSQL database for the Fraud Detection Platform.

## 📝 Files

### `schema.sql`
- Contains the DDL (Data Definition Language) statements to create the database schema.
- Tables included:
    - **users**: System users and roles.
    - **api_keys**: API keys for external access.
    - **analysis_logs**: Logs of fraud analysis requests.
        - Supports `TEXT`, `URL`, `DOCUMENT`, `IMAGE`, `MULTIMODAL`.
    - **risk_components**: Breakdown of risk scores.
        - Includes `text_score`, `url_score`, `metadata_score`, `malware_score`.
    - **alerts**: Notification records.
    - **audit_logs**: System audit trail.

### `seed_data.sql`
- Contains initial data for testing and development.
- Creates default users:
    - Admin (`admin@fraudplatform.com`)
    - Analyst (`analyst@fraudplatform.com`)
    - Client (`client@fraudplatform.com`) with a valid API key.

## 🛠️ Usage

### Initialization
To initialize the database, run the `init_db.py` script from the project root:
```bash
python init_db.py
```

### Resetting
To **destroy** the database and re-create it (useful during development after schema changes):
```bash
python reset_db.py
```
*Warning: This deletes all data!*
