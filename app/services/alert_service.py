import logging
from datetime import datetime
from app.core.database import SessionLocal
from app.domain.models import Alert
from app.core.kafka_client import KafkaClient
from app.core.config import Config

logger = logging.getLogger(__name__)

class AlertService:
    @staticmethod
    def evaluate_vitals(db, vitals):
        """
        Evaluates vitals against rules and creates alerts if thresholds are crossed.
        This runs synchronously within the request.
        """
        alerts_created = []
        
        try:
            # Rule 1: Tachycardia (HR > 130)
            if vitals.hr_bpm and vitals.hr_bpm > 130:
                severity = 'high' if vitals.hr_bpm > 150 else 'medium'
                AlertService._create_alert(
                    db, vitals, 
                    type='tachycardia', 
                    severity=severity, 
                    message=f"HR {vitals.hr_bpm} bpm (> 130): Tachycardia suspected"
                )
                alerts_created.append('tachycardia')

            # Rule 2: Hypoxia (SpO2 < 90)
            if vitals.spo2_pct and vitals.spo2_pct < 90:
                AlertService._create_alert(
                    db, vitals, 
                    type='hypoxia', 
                    severity='high', 
                    message=f"SpO₂ {vitals.spo2_pct}% (< 90%): Hypoxia suspected"
                )
                alerts_created.append('hypoxia')

            # Rule 3: Hypertension (Sys > 180 OR Dia > 110)
            sys = vitals.bp_systolic
            dia = vitals.bp_diastolic
            if (sys and sys > 180) or (dia and dia > 110):
                msg_parts = []
                if sys and sys > 180: msg_parts.append(f"Sys {sys} (> 180)")
                if dia and dia > 110: msg_parts.append(f"Dia {dia} (> 110)")
                
                AlertService._create_alert(
                    db, vitals, 
                    type='hypertension', 
                    severity='high', 
                    message=f"BP {'/'.join(msg_parts)}: Hypertension suspected"
                )
                alerts_created.append('hypertension')

            # Rule 4: Fever (Temp > 38.5)
            if vitals.temp_c and vitals.temp_c > 38.5:
                AlertService._create_alert(
                    db, vitals, 
                    type='fever', 
                    severity='medium', 
                    message=f"Temp {vitals.temp_c}°C (> 38.5): Fever suspected"
                )
                alerts_created.append('fever')
                
            if alerts_created:
                db.commit()
                
        except Exception as e:
            logger.error(f"Error evaluating alerts for vitals {vitals.id}: {e}")
            # Do not re-raise, we don't want to fail the vitals ingestion
            
        return alerts_created

    @staticmethod
    def _create_alert(db, vitals, type, severity, message):
        alert = Alert(
            patient_id=vitals.patient_id,
            encounter_id=vitals.encounter_id,
            timestamp=vitals.timestamp,
            type=type,
            severity=severity,
            message=message,
            resolved=False
        )
        db.add(alert)
        # We need to flush to get the ID for Kafka, but commit happens in caller or later
        db.flush() 
        
        # Publish to Kafka
        try:
            alert_payload = {
                'alert_id': alert.id,
                'patient_id': alert.patient_id,
                'encounter_id': alert.encounter_id,
                'type': alert.type,
                'severity': alert.severity,
                'message': alert.message,
                'created_at': datetime.utcnow().isoformat()
            }
            KafkaClient.send_message(Config.KAFKA_TOPIC_ALERTS, alert_payload)
        except Exception as e:
            logger.error(f"Failed to publish alert to Kafka: {e}")
