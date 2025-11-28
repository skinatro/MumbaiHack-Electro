import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Application configuration.
    Reads from environment variables or defaults to development settings.
    """
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Database connection string (PostgreSQL)
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg://admin:password@localhost:5432/hospital_db')
    
    # Kafka configuration
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(',')
    KAFKA_TOPIC_VITALS = os.getenv('KAFKA_TOPIC_VITALS', 'vitals_stream')
    KAFKA_TOPIC_ALERTS = os.getenv('KAFKA_TOPIC_ALERTS', 'alerts')
