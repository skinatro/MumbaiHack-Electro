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

## Project Structure

- `app/api`: API route handlers (Blueprints).
- `app/core`: Core configuration, database, security, and utilities.
- `app/domain`: SQLAlchemy models.
- `app/repositories`: Data access layer.
- `app/schemas`: Pydantic models for validation.
- `app/services`: Business logic (Rule Engine).
