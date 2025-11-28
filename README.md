# Hospital Backend System

A production-grade backend for a hospital management system, built with Flask, PostgreSQL, and Kafka.

## Features

- **Authentication**: JWT-based auth with role-based access control (RBAC).
- **Encounters**: Manage patient admissions and room assignments.
- **Vitals**: Ingest patient vitals via REST, publish to Kafka, and run rule-based alerts.
- **Observations**: Record doctor/nurse observations.
- **Logging**: Request logging and global error handling.
- **Validation**: Strict input validation using Pydantic schemas.

## Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)

## Setup & Running

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd MumbaiHack-Electro
   ```

2. **Start services with Docker Compose**
   ```bash
   docker-compose up -d
   ```
   This will start PostgreSQL, Zookeeper, and Kafka.

3. **Run Migrations**
   (Assuming you have `alembic` or similar set up, or just let the app create tables on startup if configured. For this setup, we'll assume `app.core.database` handles it or you run a script.)
   
   *Note: Ensure the database is ready before running the app.*

4. **Run the Application (Local)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python app/app.py
   ```
   The API will be available at `http://localhost:5001`.

## API Usage

### Authentication

**Login**
```bash
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

**Get Current User**
```bash
curl -X GET http://localhost:5001/auth/me \
  -H "Authorization: Bearer <token>"
```

### Encounters

**Admit Patient**
```bash
curl -X POST http://localhost:5001/encounters \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"patient_id": 1, "doctor_id": 2}'
```

### Vitals

**Ingest Vitals**
```bash
curl -X POST http://localhost:5001/vitals \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "encounter_id": 10,
    "timestamp": "2023-10-27T10:00:00Z",
    "hr_bpm": 80,
    "spo2_pct": 98,
    "temp_c": 37.0
  }'
```

### Observations

**Create Observation**
```bash
curl -X POST http://localhost:5001/observations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"encounter_id": 10, "note": "Patient looks stable."}'
```

## Endpoints for Frontend Team

### Doctor View

**Get Doctor's Patients**
Returns active encounters for the authenticated doctor.
```bash
curl -X GET http://localhost:5001/doctors/<doctor_id>/patients \
  -H "Authorization: Bearer <token>"
```
Response:
```json
{
  "status": "success",
  "data": {
    "encounters": [
      {
        "id": 101,
        "patient": { "id": 1, "name": "Patient 1", "age": null, "gender": "M" },
        "room": { "id": 5, "room_number": "101A" },
        "admitted_at": "2023-10-27T10:00:00",
        "status": "active"
      }
    ]
  }
}
```

**Get Encounter Overview**
Returns comprehensive status for a specific encounter.
```bash
curl -X GET http://localhost:5001/encounters/<encounter_id>/overview \
  -H "Authorization: Bearer <token>"
```
Response:
```json
{
  "status": "success",
  "data": {
    "encounter_id": 101,
    "patient_id": 1,
    "latest_vitals": {
      "timestamp": "2023-10-27T10:05:00",
      "hr_bpm": 80,
      "spo2_pct": 98,
      "temp_c": 37.0,
      "bp_systolic": 120,
      "bp_diastolic": 80,
      "resp_rate": 16
    },
    "last_observation": {
      "id": 50,
      "note": "Patient resting comfortably.",
      "created_at": "2023-10-27T09:00:00",
      "author_id": 2
    },
    "alerts_count": 0,
    "status": "active"
  }
}
```

### Patient View

**Get Current Encounter**
Returns the active encounter for the authenticated patient.
```bash
curl -X GET http://localhost:5001/patients/<patient_id>/encounter \
  -H "Authorization: Bearer <token>"
```

**Get Recent Vitals**
Returns the last N vitals data points.
```bash
curl -X GET http://localhost:5001/patients/<patient_id>/vitals/recent?limit=10 \
  -H "Authorization: Bearer <token>"
```

### Alerts & Monitoring API

**Rules**
- **Tachycardia**: HR > 130 bpm
- **Hypoxia**: SpO₂ < 90%
- **Hypertension**: Systolic > 180 OR Diastolic > 110
- **Fever**: Temp > 38.5°C

**List Encounter Alerts**
```bash
curl -X GET http://localhost:5001/encounters/<encounter_id>/alerts \
  -H "Authorization: Bearer <token>"
```

**Resolve Alert**
```bash
curl -X PATCH http://localhost:5001/alerts/<alert_id>/resolve \
  -H "Authorization: Bearer <token>"
```

**Get Recent Doctor Alerts**
```bash
curl -X GET http://localhost:5001/doctors/me/alerts/recent \
  -H "Authorization: Bearer <token>"
```

## Alert Engine

The Alert Engine runs synchronously within the Vitals Ingestion API. When vitals are posted, they are evaluated against the rules, and alerts are created immediately if thresholds are crossed. Alerts are also published to Kafka (`alerts` topic).

**Example Alert JSON (Kafka Event)**
```json
{
  "alert_id": 10,
  "patient_id": 1,
  "encounter_id": 2,
  "type": "tachycardia",
  "severity": "high",
  "message": "HR 145 bpm (> 130): Tachycardia suspected",
  "created_at": "2023-10-27T10:05:00"
}
```

## Vitals Simulator

A standalone script is provided to simulate a medical device sending vitals to the backend. It generates realistic data and occasionally injects anomalies to trigger alerts.

**Configuration**
Set the following in your `.env` file (or use defaults):
```bash
BACKEND_URL=http://localhost:5001
SIM_DOCTOR_USERNAME=admin
SIM_DOCTOR_PASSWORD=password
SIM_PATIENT_ID=1      # ID of an existing patient
SIM_ENCOUNTER_ID=2    # ID of an active encounter for that patient
```

**Running the Simulator**
```bash
python scripts/vitals_simulator.py
```

**Output Example**
```text
Logging in to http://localhost:5001/auth/login as admin...
Login successful.
Starting simulation for Patient 1, Encounter 1
Press Ctrl+C to stop.
[10:05:00] Sent: HR=85, SpO2=98, Temp=37.1 -> Status: 201
[10:05:08] Sent: HR=92, SpO2=97, Temp=36.9 -> Status: 201
!!! Injecting ANOMALY: tachycardia !!!
[10:05:16] Sent: HR=155, SpO2=96, Temp=37.0 -> Status: 201
   >>> ALERTS TRIGGERED: ['tachycardia']
```
   >>> ALERTS TRIGGERED: ['tachycardia']
```
This is useful for demonstrating real-time monitoring and alert generation on the frontend.

## Auto-Admission Agent

The system includes an intelligent agent for handling patient admissions automatically.

**Endpoint**: `POST /admissions/auto`

**Request Example**:
```json
{
  "name": "John Doe",
  "age": 45,
  "gender": "Male",
  "symptoms": ["severe chest pain", "sweating"],
  "complaint_description": "Patient collapsed at home",
  "severity_hint": "high"
}
```

**Response Example**:
```json
{
  "status": "success",
  "data": {
    "encounter_id": 10,
    "patient_id": 5,
    "room_id": 2,
    "room_number": "102",
    "department": "ICU",
    "status": "active",
    "assigned_doctor_id": 1,
    "triage_decision": "ICU",
    "notes": "Admitted to ICU (Triage: ICU). Reason: severe chest pain"
  },
  "error": null
}
```

**Logic**:
1. **Triage**: Keywords like "chest pain", "unconscious" -> ICU. Mild symptoms -> General.
2. **Room Allocation**: Finds first free room in the triaged department. Falls back to General if ICU is full.
3. **User Creation**: Automatically creates a User and Patient profile if they don't exist.
4. **Encounter**: Creates an active encounter assigned to a doctor.

## Auto-Discharge System

The system monitors patient stability and automatically discharges them when criteria are met, generating a comprehensive discharge plan.

**Endpoints**:
- `POST /discharge/auto/run`: Trigger auto-discharge evaluation for all active encounters.
- `PATCH /encounters/<id>/discharge`: Manually discharge an encounter (Doctor/Admin).
- `GET /encounters/<id>/discharge_plan`: Fetch the generated discharge plan.
- `GET /patients/me/post_discharge`: Fetch the logged-in patient's latest discharge plan.

**Stability Rules**:
- **Time**: Admitted for at least 2 days (configurable).
- **Alerts**: No high severity alerts in the last 12 hours.
- **Vitals**: Last 24 hours of vitals must be within normal ranges (HR 60-110, SpO2 >= 94, BP <= 150/95, Temp <= 37.8).

**Discharge Plan (LLM-Generated)**:
Includes a summary, home care instructions, recommended medications, and follow-up schedule.

## LLM Doctor Copilot

A dedicated service that analyzes alerts and provides structured, AI-generated explanations to assist doctors.

**Features**:
- Listens to Kafka `alerts` topic.
- Fetches patient context and recent vitals.
- Generates summary, risk level, suggested checks, and actions using LLM.
- Exposes explanation via API.

**Endpoint**:
- `GET /alerts/<id>/explanation`: Fetch the copilot's analysis for a specific alert.

## LLM / Ollama Healthcheck

Verify the LangChain + Ollama integration.

**Environment Variables**:
- `OLLAMA_BASE_URL`: URL of the Ollama instance (default: `http://localhost:11434`).
- `OLLAMA_MODEL`: Model to use (default: `llama3`).

**Endpoints**:
- `GET /llm/health`: Checks connectivity to Ollama. Returns `200` and `"ok": true` if successful.
- `GET /llm/copilot/smoke_test`: Runs a smoke test of the doctor copilot pipeline using a fake context.

## Project Structure

- `app/api`: API route handlers (Blueprints).
- `app/core`: Core configuration, database, security, and utilities.
- `app/domain`: SQLAlchemy models.
- `app/repositories`: Data access layer.
- `app/schemas`: Pydantic models for validation.
- `app/services`: Business logic (Rule Engine).
