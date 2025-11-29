# 🏥 MumbaiHack-Electro: Next-Gen Agentic Hospital Management

> **Winner of MumbaiHack 2024 (Hopefully!)** 🏆
>
> A fully "Agentic" hospital management system that uses AI to automate admissions, monitor vitals in real-time, assist doctors with LLM-powered insights, and manage patient discharge.

---

## 🚀 The Problem
Traditional hospital systems are static data repositories. Doctors are overwhelmed with raw data, admissions are manual bottlenecks, and discharge planning is often delayed.

## 💡 The Solution: Agentic AI
**MumbaiHack-Electro** transforms the hospital into an active, intelligent system. It doesn't just store data; it **acts** on it.

### ✨ Key "Agentic" Features

1.  **🤖 Auto-Admission Agent**
    *   **What it does:** Uses NLP to analyze patient complaints, automatically triages them (ICU vs. General), assigns the appropriate room, and creates the encounter.
    *   **Tech:** LangChain + Rule Engine.

2.  **❤️ Real-Time Vitals Monitoring**
    *   **What it does:** Ingests high-frequency vitals (HR, SpO2, BP) via Kafka streams.
    *   **Alerts:** Instantly triggers alerts for conditions like Tachycardia, Hypoxia, or Fever based on medical rules.

3.  **🧠 LLM Doctor Copilot**
    *   **What it does:** When an alert triggers, the Copilot analyzes the patient's history and current vitals to provide a **structured clinical explanation**, risk assessment, and suggested actions.
    *   **Tech:** Ollama (Llama 3) + RAG.

4.  **✅ Auto-Discharge Agent**
    *   **What it does:** Continuously monitors patient stability (vitals trends + alert history). When criteria are met, it drafts a complete discharge plan including home care instructions and meds.

---

## 🛠️ Tech Stack

*   **Frontend:** React, Tailwind CSS, Recharts (Real-time dashboards)
*   **Backend:** Flask (Python), SQLAlchemy
*   **Streaming:** Apache Kafka, Zookeeper
*   **Database:** PostgreSQL
*   **AI/LLM:** Ollama, LangChain

---

## ⚡ Quick Start

### 1. Backend & Infrastructure (Docker)
Start the database, Kafka, and backend services.

```bash
# Clone the repo
git clone <repo-url>
cd MumbaiHack-Electro

# Start services
docker-compose up -d
```
*Wait for a minute for Kafka and Postgres to initialize.*

### 2. Frontend (React)
Launch the doctor/patient dashboard.

```bash
# Install dependencies
npm install

# Run dev server
npm run dev
```
Access the UI at: `http://localhost:5173`

### 3. Vitals Simulator (Optional but Recommended)
Simulate a medical device sending real-time data to see the charts move!

```bash
# Create a virtual env for the script if needed
python3 -m venv venv
source venv/bin/activate
pip install requests

# Run the simulator
python scripts/vitals_simulator.py
```

---

## 🎮 Demo Walkthrough for Judges

1.  **Login as Doctor**
    *   Go to `http://localhost:5173`
    *   Login: `admin` / `password` (or any seeded doctor credentials)
    *   **View Dashboard:** See active patients and recent alerts.

2.  **Auto-Admission**
    *   Click **"Admit Patient"**.
    *   Enter a complaint like: *"Severe chest pain and difficulty breathing since morning."*
    *   **Watch the Agent:** It will auto-select **ICU**, assign a room, and create the profile.

3.  **Real-Time Monitoring**
    *   Open the **Encounter Detail** for a patient.
    *   Run the `vitals_simulator.py` script in a terminal.
    *   **Watch:** The charts update in real-time.
    *   **Trigger Anomaly:** The simulator will eventually send abnormal data (or you can force it).

4.  **AI Copilot**
    *   When an alert appears (e.g., "Tachycardia"), click it.
    *   See the **AI Explanation**: The LLM explains *why* this is happening and suggests checking specific medications or labs.

5.  **Auto-Discharge**
    *   For a stable patient, click **"Check Discharge Eligibility"**.
    *   If stable, the Agent generates a **Discharge Plan**.
    *   View the plan: Summary, Meds, and Follow-up instructions.

---

## 📸 Screenshots

*(Add screenshots of Dashboard, Vitals Chart, and Copilot here)*

---

Made with ❤️ by Team Electro for MumbaiHack 2024
