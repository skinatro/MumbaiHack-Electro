-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'doctor', 'patient')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Doctors table
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    specialty VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Patients table
CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    dob DATE,
    gender VARCHAR(10),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Rooms table
CREATE TABLE IF NOT EXISTS rooms (
    id SERIAL PRIMARY KEY,
    room_number VARCHAR(20) UNIQUE NOT NULL,
    department VARCHAR(50),
    is_occupied BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Encounters table
CREATE TABLE IF NOT EXISTS encounters (
    id SERIAL PRIMARY KEY,
    patient_id INTEGER REFERENCES patients(id),
    doctor_id INTEGER REFERENCES doctors(id),
    room_id INTEGER REFERENCES rooms(id),
    status VARCHAR(20) CHECK (status IN ('active', 'discharged')),
    admitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    discharged_at TIMESTAMP WITH TIME ZONE
);

-- Vitals table (Time-series data)
CREATE TABLE IF NOT EXISTS vitals (
    id SERIAL PRIMARY KEY,
    encounter_id INTEGER REFERENCES encounters(id),
    patient_id INTEGER REFERENCES patients(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    hr_bpm INTEGER,
    spo2_pct INTEGER,
    resp_rate_bpm INTEGER,
    bp_systolic INTEGER,
    bp_diastolic INTEGER,
    temp_c DECIMAL(4, 1),
    device_flags TEXT[]
);

-- Observations table
CREATE TABLE IF NOT EXISTS observations (
    id SERIAL PRIMARY KEY,
    encounter_id INTEGER REFERENCES encounters(id),
    author_id INTEGER REFERENCES users(id),
    note TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for time-series queries
CREATE INDEX IF NOT EXISTS idx_vitals_patient_time ON vitals(patient_id, timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_vitals_encounter_time ON vitals(encounter_id, timestamp DESC);
