import json
from kafka import KafkaProducer
from app.core.config import Config
import logging

logger = logging.getLogger(__name__)

class KafkaClient:
    _producer = None

    @classmethod
    def get_producer(cls):
        if cls._producer is None:
            try:
                cls._producer = KafkaProducer(
                    bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                    api_version=(2, 0, 0) # Fix for UnrecognizedBrokerVersion
                )
                logger.info("Kafka producer initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka producer: {e}")
        return cls._producer

    @classmethod
    def send_message(cls, topic, message):
        producer = cls.get_producer()
        if producer:
            try:
                producer.send(topic, message)
                producer.flush()
                logger.info(f"Sent message to {topic}")
            except Exception as e:
                logger.error(f"Failed to send message to {topic}: {e}")
        else:
            logger.warning("Kafka producer not available, skipping message")
