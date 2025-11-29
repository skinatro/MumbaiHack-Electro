# MumbaiHack-Electro Backend Demo Script

This document outlines the steps to demonstrate the full capabilities of the Hospital Monitoring Backend.

## Prerequisites

1.  **Docker Services**: Ensure PostgreSQL, Kafka, and Zookeeper are running.
    ```bash
    docker-compose up -d
    ```
2.  **Ollama**: Ensure Ollama is running locally with `llama3` (or configured model).
    ```bash
    ollama run llama3
    ```
3.  **Virtual Environment**:
    ```bash
    source venv/bin/activate
    ```

## 1. Setup & Seeding

Reset the database and seed it with rich demo data (Doctors, Patients, Encounters, History).

```bash
# Run the seed script
python scripts/seed.py
```

**What to show:**
*   Database tables populated.
*   Users `admin`, `dr_house`, `patient_zero` created.
*   Active encounter for `patient_zero`.
*   Discharged encounter for `alice_wonder` with a generated plan.

## 2. Infrastructure Healthcheck

Verify that the backend and AI infrastructure are operational.

```bash
# Start the backend (if not running) on port 5001
python -m app.app
```

**In a separate terminal:**
```bash
# Check LLM connectivity
curl http://localhost:5001/llm/health
# Expected: {"status": "success", "data": {"ok": true, ...}}
```

## 3. Real-time Monitoring & Alerts (The "Sepsis" Scenario)

Simulate a patient deteriorating to trigger alerts and AI analysis.

**Step A: Start Simulator**
```bash
# Simulate Patient Zero (ID: 1) in Encounter (ID: 1) with 'sepsis' scenario
python tests/simulator.py 1 1 --scenario sepsis
```

**Step B: Observe Backend Logs**
*   Watch for `POST /vitals` requests.
*   Watch for `!!! ALERT GENERATED !!!` in simulator output.
*   Watch for `Generating alert explanation...` in backend logs (Copilot kicking in).

**Step C: Verify Data via API**
```bash
# Login as Doctor
TOKEN=$(curl -s -X POST http://localhost:5001/auth/login -H 'Content-Type: application/json' -d '{"username": "dr_house", "password": "password"}' | grep -oP '"access_token":\s*"\K[^"]+')

# Get Recent Alerts
curl -H "Authorization: Bearer $TOKEN" http://localhost:5001/doctors/me/alerts/recent
```

## 4. AI Doctor Copilot

Show the AI-generated explanation for the alert triggered above.

```bash
# Get the Alert ID from the previous step's output (e.g., ID 2)
ALERT_ID=2

# Fetch Explanation
curl -H "Authorization: Bearer $TOKEN" http://localhost:5001/alerts/$ALERT_ID/explanation
```
**What to show:**
*   JSON response with `summary`, `risk_level`, `suggested_actions`.
*   Note the safety disclaimer.

## 5. Auto-Admission & Triage

Demonstrate the intelligent admission agent.

```bash
curl -X POST http://localhost:5001/admissions/auto \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 55,
    "gender": "Male",
    "symptoms": ["crushing chest pain", "shortness of breath"],
    "complaint_description": "Collapsed at work",
    "severity_hint": "high"
  }'
```
**What to show:**
*   Response shows `triage_decision: ICU`.
*   Room assigned in ICU department.
*   New patient and encounter created.

## 6. Discharge & Recovery

Demonstrate the discharge workflow.

**Step A: Simulate Recovery**
```bash
# Switch simulator to recovery mode (or stop and restart)
python tests/simulator.py 1 1 --scenario recovery
```

**Step B: Manual Discharge with Plan Generation**
```bash
# Discharge Patient Zero
curl -X PATCH http://localhost:5001/encounters/1/discharge \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"generate_plan": true}'
```

**Step C: View Discharge Plan**
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:5001/encounters/1/discharge_plan
```
**What to show:**
*   Structured discharge plan with meds and instructions.

## 7. Patient Portal (RBAC Check)

Verify that patients can only see their own data.

```bash
# Login as Patient Zero
P_TOKEN=$(curl -s -X POST http://localhost:5001/auth/login -H 'Content-Type: application/json' -d '{"username": "patient_zero", "password": "password"}' | grep -oP '"access_token":\s*"\K[^"]+')

# Try to access Alice's encounter (ID 2) -> Should Fail
curl -H "Authorization: Bearer $P_TOKEN" http://localhost:5001/encounters/2
# Expected: 403 Unauthorized

# Access Own Encounter (ID 1) -> Should Succeed
curl -H "Authorization: Bearer $P_TOKEN" http://localhost:5001/encounters/1
```
