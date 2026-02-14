-- Seed Data for AI-Driven Multi-Modal Fraud Detection Platform

-- Insert initial admin user
-- Password is 'admin123' hashed with bcrypt (example hash, in production use proper hashing)
INSERT INTO users (id, name, email, hashed_password, role)
VALUES 
    (uuid_generate_v4(), 'System Admin', 'admin@fraudplatform.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'BANK_ADMIN'),
    (uuid_generate_v4(), 'SOC Analyst', 'analyst@fraudplatform.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'SOC_ANALYST'),
    (uuid_generate_v4(), 'API Client', 'client@fraudplatform.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'USER');

-- Insert initial API Key for the API Client
INSERT INTO api_keys (user_id, api_key, status, expires_at)
SELECT id, 'fp_live_init_key_12345', 'ACTIVE', NOW() + INTERVAL '1 year'
FROM users
WHERE email = 'client@fraudplatform.com';
