import os
import time
import random
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:5001")
USERNAME = os.getenv("SIM_DOCTOR_USERNAME", "admin") # Default to admin if not set
PASSWORD = os.getenv("SIM_DOCTOR_PASSWORD", "admin123")
PATIENT_ID = int(os.getenv("SIM_PATIENT_ID", "1"))
ENCOUNTER_ID = int(os.getenv("SIM_ENCOUNTER_ID", "2"))

class VitalsSimulator:
    def __init__(self):
        self.token = None
        self.headers = {"Content-Type": "application/json"}

    def login(self):
        """Authenticates with the backend and retrieves a JWT."""
        url = f"{BACKEND_URL}/auth/login"
        payload = {"username": USERNAME, "password": PASSWORD}
        
        try:
            print(f"Logging in to {url} as {USERNAME}...")
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "success":
                self.token = data["data"]["access_token"]
                self.headers["Authorization"] = f"Bearer {self.token}"
                print("Login successful.")
            else:
                print(f"Login failed: {data.get('error')}")
                exit(1)
        except Exception as e:
            print(f"Login error: {e}")
            exit(1)

    def generate_vitals(self, iteration):
        """Generates vitals data, occasionally injecting anomalies."""
        
        # Default normal ranges
        hr = random.randint(70, 110)
        spo2 = random.randint(95, 99)
        resp = random.randint(12, 20)
        sys = random.randint(110, 140)
        dia = random.randint(70, 90)
        temp = round(random.uniform(36.5, 37.8), 1)
        
        # Inject anomalies every ~10th iteration (randomized)
        if iteration % 10 == 0 or random.random() < 0.1:
            anomaly_type = random.choice(["tachycardia", "hypoxia", "fever", "hypertension"])
            print(f"!!! Injecting ANOMALY: {anomaly_type} !!!")
            
            if anomaly_type == "tachycardia":
                hr = random.randint(140, 160)
            elif anomaly_type == "hypoxia":
                spo2 = random.randint(85, 89)
            elif anomaly_type == "fever":
                temp = round(random.uniform(38.5, 39.5), 1)
            elif anomaly_type == "hypertension":
                sys = random.randint(185, 200)
                dia = random.randint(115, 130)

        return {
            "patient_id": PATIENT_ID,
            "encounter_id": ENCOUNTER_ID,
            "timestamp": datetime.utcnow().isoformat(),
            "hr_bpm": hr,
            "spo2_pct": spo2,
            "resp_rate_bpm": resp,
            "bp_systolic": sys,
            "bp_diastolic": dia,
            "temp_c": temp,
            "device_flags": ["sensor_ok"]
        }

    def run(self):
        """Main loop to send vitals."""
        self.login()
        
        iteration = 0
        url = f"{BACKEND_URL}/vitals"
        
        print(f"Starting simulation for Patient {PATIENT_ID}, Encounter {ENCOUNTER_ID}")
        print("Press Ctrl+C to stop.")
        
        try:
            while True:
                iteration += 1
                vitals = self.generate_vitals(iteration)
                
                try:
                    # Note: /vitals endpoint might not require auth for devices, 
                    # but if it does, headers are set.
                    # Based on codebase, it's currently open or requires auth depending on config.
                    # We send headers just in case.
                    response = requests.post(url, json=vitals, headers=self.headers)
                    
                    status = response.status_code
                    try:
                        resp_data = response.json()
                        alerts = resp_data.get("data", {}).get("alerts", [])
                    except:
                        alerts = []
                        
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent: HR={vitals['hr_bpm']}, SpO2={vitals['spo2_pct']}, Temp={vitals['temp_c']} -> Status: {status}")
                    
                    if alerts:
                        print(f"   >>> ALERTS TRIGGERED: {alerts}")
                        
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
                
                time.sleep(random.uniform(5, 10))
                
        except KeyboardInterrupt:
            print("\nSimulation stopped.")

if __name__ == "__main__":
    sim = VitalsSimulator()
    sim.run()
