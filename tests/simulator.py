import requests
import time
import random
import datetime
import json
import argparse
import sys

API_URL = "http://localhost:5001/vitals"

def get_normal_vitals():
    return {
        "hr_bpm": random.randint(60, 100),
        "spo2_pct": random.randint(95, 100),
        "resp_rate_bpm": random.randint(12, 20),
        "bp_systolic": random.randint(110, 130),
        "bp_diastolic": random.randint(70, 85),
        "temp_c": round(random.uniform(36.5, 37.5), 1),
        "device_flags": []
    }

def get_sepsis_vitals():
    return {
        "hr_bpm": random.randint(110, 140), # Tachycardia
        "spo2_pct": random.randint(88, 94), # Hypoxia
        "resp_rate_bpm": random.randint(22, 30), # Tachypnea
        "bp_systolic": random.randint(80, 100), # Hypotension
        "bp_diastolic": random.randint(50, 65),
        "temp_c": round(random.uniform(38.5, 40.0), 1), # Fever
        "device_flags": []
    }

def get_recovery_vitals(step, total_steps=20):
    # Interpolate from Sepsis to Normal
    progress = min(step / total_steps, 1.0)
    
    sepsis = get_sepsis_vitals()
    normal = get_normal_vitals()
    
    def interpolate(start, end, p):
        return int(start + (end - start) * p)
        
    return {
        "hr_bpm": interpolate(sepsis["hr_bpm"], normal["hr_bpm"], progress),
        "spo2_pct": interpolate(sepsis["spo2_pct"], normal["spo2_pct"], progress),
        "resp_rate_bpm": interpolate(sepsis["resp_rate_bpm"], normal["resp_rate_bpm"], progress),
        "bp_systolic": interpolate(sepsis["bp_systolic"], normal["bp_systolic"], progress),
        "bp_diastolic": interpolate(sepsis["bp_diastolic"], normal["bp_diastolic"], progress),
        "temp_c": round(sepsis["temp_c"] + (normal["temp_c"] - sepsis["temp_c"]) * progress, 1),
        "device_flags": []
    }

def simulate_device(patient_id, encounter_id, scenario="normal"):
    print(f"Starting simulation for Patient {patient_id} (Encounter {encounter_id}) - Scenario: {scenario}")
    
    step = 0
    while True:
        if scenario == "sepsis":
            vitals = get_sepsis_vitals()
        elif scenario == "recovery":
            vitals = get_recovery_vitals(step)
            step += 1
        else:
            vitals = get_normal_vitals()
            
        data = {
            "patient_id": patient_id,
            "encounter_id": encounter_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            **vitals
        }
        
        try:
            response = requests.post(API_URL, json=data)
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sent: HR={data['hr_bpm']}, SpO2={data['spo2_pct']}, Temp={data['temp_c']} -> Status: {response.status_code}")
            
            if response.status_code == 201:
                resp_json = response.json()
                alerts = resp_json.get('data', {}).get('alerts', [])
                if alerts:
                     print(f"   >>> ALERTS TRIGGERED: {[a['type'] for a in alerts]}")
        except Exception as e:
            print(f"Error sending data: {e}")
        
        time.sleep(2) # Faster updates for demo

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vitals Simulator")
    parser.add_argument("patient_id", type=int, help="Patient ID")
    parser.add_argument("encounter_id", type=int, help="Encounter ID")
    parser.add_argument("--scenario", type=str, default="normal", choices=["normal", "sepsis", "recovery"], help="Simulation scenario")
    
    args = parser.parse_args()
    
    simulate_device(args.patient_id, args.encounter_id, args.scenario)
