import json
import logging
from kafka import KafkaConsumer
from app.core.config import Config
from app.core.database import SessionLocal
from app.services.rule_engine import RuleEngine
from app.domain.models import Alert
from app.core.kafka_client import KafkaClient
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_alert_engine():
    logger.info("Starting Alert Engine...")
    
    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        Config.KAFKA_TOPIC_VITALS,
        bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        auto_offset_reset='latest',
        group_id='alert_engine_group'
    )
    
    logger.info(f"Listening on topic: {Config.KAFKA_TOPIC_VITALS}")
    
    for message in consumer:
        try:
            vitals_data = message.value
            logger.info(f"Received vitals: {vitals_data}")
            
            # Evaluate Rules
            alerts = RuleEngine.evaluate(vitals_data)
            
            if alerts:
                db = SessionLocal()
                try:
                    for alert_data in alerts:
                        # Persist to DB
                        alert = Alert(
                            patient_id=alert_data['patient_id'],
                            encounter_id=vitals_data.get('encounter_id'), # Ensure encounter_id is passed in vitals
                            timestamp=datetime.fromisoformat(alert_data['timestamp']),
                            type=alert_data['type'],
                            severity=alert_data.get('severity', 'medium'),
                            details=alert_data['message'],
                            resolved=False
                        )
                        db.add(alert)
                        
                        # Publish to Kafka
                        KafkaClient.send_message(Config.KAFKA_TOPIC_ALERTS, alert_data)
                        
                    db.commit()
                    logger.info(f"Processed {len(alerts)} alerts")
                except Exception as e:
                    logger.error(f"Error processing alerts: {e}")
                    db.rollback()
                finally:
                    db.close()
                    
        except Exception as e:
            logger.error(f"Error consuming message: {e}")

if __name__ == "__main__":
    run_alert_engine()
