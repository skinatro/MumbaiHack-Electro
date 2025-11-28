import json
import logging
from kafka import KafkaConsumer
from sqlalchemy.orm import Session
from app.core.config import Config
from app.core.database import SessionLocal
from app.domain.models import Alert, AlertExplanation, Vitals, Patient, Encounter
from app.services.llm_service import LLMService
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AlertCopilotService:
    def __init__(self):
        self.consumer = None
        try:
            self.consumer = KafkaConsumer(
                Config.KAFKA_TOPIC_ALERTS,
                bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                group_id='alert_copilot_group',
                auto_offset_reset='latest',
                api_version=(2, 0, 0) # Fix for UnrecognizedBrokerVersion
            )
            logger.info("Alert Copilot Kafka consumer initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")

    def start(self):
        """
        Starts listening to alerts and processing them.
        """
        if not self.consumer:
            logger.error("Kafka consumer not initialized")
            return

        logger.info("Alert Copilot started listening...")
        for message in self.consumer:
            try:
                alert_data = message.value
                logger.info(f"Received alert: {alert_data}")
                self.process_alert(alert_data)
            except Exception as e:
                logger.error(f"Error processing alert: {e}")

    def process_alert(self, alert_data: dict):
        """
        Fetches context, calls LLM, and saves explanation.
        """
        db = SessionLocal()
        try:
            # 1. Fetch Alert from DB (to ensure it exists and get ID if not in payload)
            # Payload usually has data, but let's check.
            # Assuming payload matches AlertService publishing format: 
            # { "patient_id": ..., "encounter_id": ..., "type": ..., "severity": ..., "message": ..., "timestamp": ... }
            # Wait, AlertService publishes the DICT representation. It might NOT have the DB ID if published before commit/refresh?
            # Actually AlertService.evaluate_vitals does:
            # db.commit(); db.refresh(alert); ... send_message(..., alert_dict)
            # So alert_dict should have 'id'.
            
            alert_id = alert_data.get("id")
            if not alert_id:
                logger.warning("Alert data missing ID, skipping explanation generation")
                return

            alert = db.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                logger.warning(f"Alert {alert_id} not found in DB")
                return
                
            # Check if explanation already exists
            if alert.explanation:
                logger.info(f"Explanation already exists for alert {alert_id}")
                return

            # 2. Fetch Context
            # Patient details
            patient = db.query(Patient).filter(Patient.id == alert.patient_id).first()
            patient_age = datetime.utcnow().year - patient.dob.year if patient and patient.dob else "Unknown"
            gender = patient.gender if patient else "Unknown"
            
            # Recent vitals (last 1 hour)
            since = datetime.utcnow() - timedelta(hours=1)
            recent_vitals = db.query(Vitals).filter(
                Vitals.encounter_id == alert.encounter_id,
                Vitals.timestamp >= since
            ).order_by(Vitals.timestamp.desc()).limit(5).all()
            
            vitals_summary = [
                {"hr": v.hr_bpm, "spo2": v.spo2_pct, "bp": f"{v.bp_systolic}/{v.bp_diastolic}", "temp": v.temp_c} 
                for v in recent_vitals
            ]
            
            context = {
                "alert_type": alert.type,
                "severity": alert.severity,
                "message": alert.message,
                "patient_age": patient_age,
                "gender": gender,
                "recent_vitals": vitals_summary
            }
            
            # 3. Call LLM
            explanation_data = LLMService.generate_alert_explanation_json(context)
            
            # 4. Save Explanation
            explanation = AlertExplanation(
                alert_id=alert.id,
                summary=explanation_data.get("summary"),
                risk_level=explanation_data.get("risk_level"),
                suggested_checks=json.dumps(explanation_data.get("suggested_checks")),
                suggested_actions=json.dumps(explanation_data.get("suggested_actions"))
            )
            db.add(explanation)
            db.commit()
            logger.info(f"Generated explanation for alert {alert_id}")
            
        except Exception as e:
            logger.error(f"Failed to process alert {alert_data}: {e}")
            db.rollback()
        finally:
            db.close()

if __name__ == "__main__":
    # For testing/running directly
    service = AlertCopilotService()
    service.start()
