-- Database Schema for AI-Driven Multi-Modal Fraud Detection Platform

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(50) CHECK (role IN ('USER', 'BANK_ADMIN', 'SOC_ANALYST')) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. API Keys Table
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) CHECK (status IN ('ACTIVE', 'REVOKED', 'EXPIRED')) DEFAULT 'ACTIVE',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);

-- 3. Analysis Logs Table
CREATE TABLE analysis_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    input_type VARCHAR(50) CHECK (input_type IN ('TEXT', 'URL', 'DOCUMENT', 'IMAGE', 'MULTIMODAL')) NOT NULL,
    input_hash VARCHAR(64) NOT NULL, -- SHA256 hash of input content
    risk_score FLOAT CHECK (risk_score >= 0 AND risk_score <= 1),
    risk_level VARCHAR(50) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH')),
    decision VARCHAR(50) CHECK (decision IN ('ALLOW', 'FLAG', 'BLOCK')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 4. Risk Components Table
CREATE TABLE risk_components (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID REFERENCES analysis_logs(id) ON DELETE CASCADE,
    text_score FLOAT DEFAULT 0,
    url_score FLOAT DEFAULT 0,
    metadata_score FLOAT DEFAULT 0, -- Suspicious metadata in images/docs
    injection_score FLOAT DEFAULT 0,
    credential_score FLOAT DEFAULT 0,
    malware_score FLOAT DEFAULT 0 -- For virus/malware detection
);

-- 5. Alerts Table
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analysis_id UUID REFERENCES analysis_logs(id) ON DELETE CASCADE,
    alert_type VARCHAR(100) NOT NULL,
    sent_to VARCHAR(255),
    status VARCHAR(50) CHECK (status IN ('PENDING', 'SENT', 'FAILED')) DEFAULT 'PENDING',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Audit Logs Table
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    action VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_api_keys_key ON api_keys(api_key);
CREATE INDEX idx_analysis_logs_user ON analysis_logs(user_id);
CREATE INDEX idx_analysis_logs_created_at ON analysis_logs(created_at);
