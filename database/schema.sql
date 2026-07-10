-- =============================================
-- SPORTS INJURY RISK DETECTION - DATABASE SCHEMA
-- Milestone 1
-- =============================================

-- Users table: stores all login accounts
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('athlete','coach','physiotherapist','sports_scientist','admin')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Athlete profiles: personal sports information
CREATE TABLE athlete_profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    sport_type VARCHAR(100),
    position VARCHAR(100),
    age INTEGER,
    height_cm FLOAT,
    weight_kg FLOAT,
    injury_history TEXT,
    training_load VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Videos: records of every uploaded video
CREATE TABLE videos (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athlete_profiles(id),
    video_filename VARCHAR(255),
    video_url VARCHAR(500),
    sport_type VARCHAR(100),
    upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'uploaded' CHECK (status IN ('uploaded','processing','completed','failed'))
);

-- Risk assessments: AI analysis results for each video
CREATE TABLE risk_assessments (
    id SERIAL PRIMARY KEY,
    video_id INTEGER REFERENCES videos(id),
    risk_score FLOAT,
    risk_category VARCHAR(50) CHECK (risk_category IN ('low','moderate','high','critical')),
    joint_angles_data TEXT,
    anomalies_detected TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);