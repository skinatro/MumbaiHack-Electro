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
                'type': 'CRITICAL',
                'message': f"High Heart Rate detected: {vitals_data['hr_bpm']} BPM",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })
            
        # Rule 2: Low SpO2
        if vitals_data.get('spo2_pct') and vitals_data['spo2_pct'] < 90:
            alerts.append({
                'type': 'CRITICAL',
                'message': f"Low SpO2 detected: {vitals_data['spo2_pct']}%",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })
            
        # Rule 3: High Temperature
        if vitals_data.get('temp_c') and vitals_data['temp_c'] > 39.0:
             alerts.append({
                'type': 'WARNING',
                'message': f"High Temperature detected: {vitals_data['temp_c']} C",
                'patient_id': vitals_data['patient_id'],
                'timestamp': vitals_data['timestamp']
            })

        # Publish alerts to Kafka
        for alert in alerts:
            logger.warning(f"Alert generated: {alert}")
            KafkaClient.send_message(Config.KAFKA_TOPIC_ALERTS, alert)
            
        return alerts
