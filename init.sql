-- Empire OS Database Schema
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    provider VARCHAR(50) NOT NULL,
    reference VARCHAR(255) UNIQUE NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    sender VARCHAR(255),
    receiver VARCHAR(255),
    status VARCHAR(50) DEFAULT 'PENDING',
    is_fraud BOOLEAN DEFAULT FALSE,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Clones table
CREATE TABLE clones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL,
    language VARCHAR(10) NOT NULL,
    niche VARCHAR(100),
    fingerprint_hash VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'ACTIVE',
    risk_score DECIMAL(5,4) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_rotated TIMESTAMP,
    metadata JSONB
);

-- Content table
CREATE TABLE contents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clone_id UUID REFERENCES clones(id),
    platform VARCHAR(50) NOT NULL,
    content_type VARCHAR(50) DEFAULT 'video',
    language VARCHAR(10),
    title TEXT NOT NULL,
    body TEXT,
    status VARCHAR(50) DEFAULT 'PUBLISHED',
    views INTEGER DEFAULT 0,
    revenue DECIMAL(15,2) DEFAULT 0.0,
    trend_score DECIMAL(5,4) DEFAULT 0.0,
    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

-- Revenue table
CREATE TABLE revenues (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    platform VARCHAR(50) NOT NULL,
    content_id UUID,
    clone_id UUID,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    rpm DECIMAL(10,2),
    views INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(100) NOT NULL,
    entity VARCHAR(100) NOT NULL,
    entity_id VARCHAR(255) NOT NULL,
    performed_by VARCHAR(255) DEFAULT 'system',
    metadata JSONB,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Simulation logs
CREATE TABLE simulation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    success BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_transactions_reference ON transactions(reference);
CREATE INDEX idx_transactions_status ON transactions(status);
CREATE INDEX idx_clones_status ON clones(status);
CREATE INDEX idx_contents_published ON contents(published_at);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);

-- Insert initial data
INSERT INTO clones (platform, language, niche, fingerprint_hash, status) VALUES
('youtube', 'en', 'crypto', 'initial-clone-1', 'ACTIVE'),
('tiktok', 'es', 'lifestyle', 'initial-clone-2', 'ACTIVE'),
('instagram', 'fr', 'fitness', 'initial-clone-3', 'ACTIVE');
