from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.repositories.vitals_repo import VitalsRepository
from app.services.rule_engine import RuleEngine
from app.core.kafka_client import KafkaClient
from app.core.config import Config
from app.core.security import login_required
from datetime import datetime

vitals_bp = Blueprint('vitals', __name__, url_prefix='/vitals')

@vitals_bp.route('', methods=['POST'])
# @login_required() # Devices might authenticate differently, but for now we'll assume some auth or internal network
def ingest_vitals():
    data = request.get_json()
    
    # Validate required fields (basic check)
    required = ['patient_id', 'encounter_id', 'timestamp']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
        
    # Parse timestamp if string
    if isinstance(data['timestamp'], str):
        data['timestamp'] = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))

    db = next(get_db())
    vitals = VitalsRepository.create_vitals(db, data)
    
    # Publish to Kafka
    vitals_payload = data.copy()
    vitals_payload['timestamp'] = vitals_payload['timestamp'].isoformat()
    KafkaClient.send_message(Config.KAFKA_TOPIC_VITALS, vitals_payload)
    
    # Run Rule Engine
    alerts = RuleEngine.evaluate(vitals_payload)
    
    return jsonify({'status': 'received', 'id': vitals.id, 'alerts_generated': len(alerts)}), 201

@vitals_bp.route('', methods=['GET'])
@login_required()
def get_vitals():
    patient_id = request.args.get('patient_id')
    encounter_id = request.args.get('encounter_id')
    last_minutes = request.args.get('last_minutes')
    
    db = next(get_db())
    vitals_list = VitalsRepository.get_vitals(db, patient_id, encounter_id, last_minutes)
    
    return jsonify([{
        'id': v.id,
        'timestamp': v.timestamp.isoformat(),
        'hr_bpm': v.hr_bpm,
        'spo2_pct': v.spo2_pct,
        'temp_c': v.temp_c
    } for v in vitals_list])
