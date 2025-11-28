import requests
import time
import random
import datetime
import json

API_URL = "http://localhost:5000/vitals"

def generate_vitals(patient_id, encounter_id):
    return {
        "patient_id": patient_id,
        "encounter_id": encounter_id,
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "hr_bpm": random.randint(60, 140), # Range includes anomalies
        "spo2_pct": random.randint(85, 100), # Range includes anomalies
        "resp_rate_bpm": random.randint(12, 25),
        "bp_systolic": random.randint(110, 140),
        "bp_diastolic": random.randint(70, 90),
        "temp_c": round(random.uniform(36.5, 39.5), 1), # Range includes anomalies
        "device_flags": []
    }

def simulate_device(patient_id, encounter_id):
    print(f"Starting simulation for Patient {patient_id} (Encounter {encounter_id})")
    while True:
        data = generate_vitals(patient_id, encounter_id)
        try:
            response = requests.post(API_URL, json=data)
            print(f"Sent vitals: HR={data['hr_bpm']}, SpO2={data['spo2_pct']} -> Status: {response.status_code}")
            if response.status_code == 201:
                resp_json = response.json()
                if resp_json.get('alerts_generated', 0) > 0:
                    print(f"!!! ALERT GENERATED !!!")
        except Exception as e:
            print(f"Error sending data: {e}")
        
        time.sleep(5)

if __name__ == "__main__":
    # You would typically get these IDs after creating a patient and encounter via the API
    # For now, we'll assume some IDs exist or you can update them manually
    import sys
    if len(sys.argv) < 3:
        print("Usage: python simulator.py <patient_id> <encounter_id>")
        sys.exit(1)
        
    p_id = int(sys.argv[1])
    e_id = int(sys.argv[2])
    simulate_device(p_id, e_id)
