from app.core.kafka_client import KafkaClient
from app.core.config import Config
import logging

logger = logging.getLogger(__name__)

class RuleEngine:
    @staticmethod
    def evaluate(vitals_data):
        alerts = []
        
        # Rule 1: High Heart Rate
        if vitals_data.get('hr_bpm') and vitals_data['hr_bpm'] > 130:
            alerts.append({
                'type': 'TACHYCARDIA',
                'severity': 'high',
                'message': f"High Heart Rate detected: {vitals_data['hr_bpm']} BPM",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })
            
        # Rule 2: Low SpO2
        if vitals_data.get('spo2_pct') and vitals_data['spo2_pct'] < 90:
            alerts.append({
                'type': 'HYPOXIA',
                'severity': 'high',
                'message': f"Low SpO2 detected: {vitals_data['spo2_pct']}%",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })
            
        # Rule 3: High Temperature
        if vitals_data.get('temp_c') and vitals_data['temp_c'] > 38.5:
             alerts.append({
                'type': 'FEVER',
                'severity': 'medium',
                'message': f"High Temperature detected: {vitals_data['temp_c']} C",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })

        # Rule 4: Hypertension
        sys = vitals_data.get('bp_systolic')
        dia = vitals_data.get('bp_diastolic')
        if (sys and sys > 180) or (dia and dia > 110):
            alerts.append({
                'type': 'HYPERTENSION',
                'severity': 'high',
                'message': f"Hypertension detected: {sys}/{dia} mmHg",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })

        # Rule 5: Bradycardia (HR < 50)
        if vitals_data.get('hr_bpm') and vitals_data['hr_bpm'] < 50:
            alerts.append({
                'type': 'BRADYCARDIA',
                'severity': 'high',
                'message': f"Bradycardia detected: {vitals_data['hr_bpm']} BPM",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })

        # Rule 6: Hypotension (Sys < 90)
        if sys and sys < 90:
            alerts.append({
                'type': 'HYPOTENSION',
                'severity': 'high',
                'message': f"Hypotension detected: {sys}/{dia} mmHg",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })

        # Rule 7: Respiratory Rate Abnormalities
        resp = vitals_data.get('resp_rate_bpm')
        if resp:
            if resp > 24:
                alerts.append({
                    'type': 'TACHYPNEA',
                    'severity': 'medium',
                    'message': f"Rapid breathing detected: {resp} bpm",
                    'patient_id': vitals_data['patient_id'],
                    'timestamp': vitals_data['timestamp']
                })
            elif resp < 8:
                alerts.append({
                    'type': 'BRADYPNEA',
                    'severity': 'high',
                    'message': f"Respiratory depression detected: {resp} bpm",
                    'patient_id': vitals_data['patient_id'],
                    'timestamp': vitals_data['timestamp']
                })

        # Rule 8: Sepsis Pattern (Temp > 38.5 AND HR > 100 AND Resp > 20)
        temp = vitals_data.get('temp_c')
        hr = vitals_data.get('hr_bpm')
        if temp and hr and resp:
            if temp > 38.5 and hr > 100 and resp > 20:
                alerts.append({
                    'type': 'SEPSIS_RISK',
                    'severity': 'critical',
                    'message': f"Possible Sepsis Pattern: Temp {temp}C, HR {hr}, Resp {resp}",
                    'patient_id': vitals_data['patient_id'],
                    'timestamp': vitals_data['timestamp']
                })

        # Rule 9: Respiratory Distress (SpO2 < 92 AND Resp > 24)
        spo2 = vitals_data.get('spo2_pct')
        if spo2 and resp:
            if spo2 < 92 and resp > 24:
                alerts.append({
                    'type': 'RESPIRATORY_DISTRESS',
                    'severity': 'critical',
                    'message': f"Respiratory Distress: SpO2 {spo2}%, Resp {resp}",
                    'patient_id': vitals_data['patient_id'],
                    'timestamp': vitals_data['timestamp']
                })

        # Publish alerts to Kafka (Optional: Consumer does it too, but maybe API ingestion needs immediate publish?)
        # The prompt says "Also publish a JSON alert event to Kafka topic alerts."
        # If the consumer does it, we might duplicate if the API also calls this.
        # The API calls RuleEngine.evaluate.
        # Let's remove the Kafka publish from here and let the caller handle it or the consumer handle it.
        # Wait, the API `ingest_vitals` calls `RuleEngine.evaluate`.
        # If we move logic to consumer, the API shouldn't need to run rules?
        # The prompt says: "Implement a separate module/service for a rule-based alert engine that consumes the vitals_stream Kafka topic."
        # This implies the API should just ingest and publish vitals. The consumer does the rules.
        # So I should REMOVE RuleEngine call from `app/api/vitals.py` later.
        # For now, I'll keep `evaluate` pure and remove side effects (Kafka publish) from here.
            
        return alerts
