from flask import Blueprint, request
from app.core.database import get_db
from app.repositories.vitals_repo import VitalsRepository
from app.services.rule_engine import RuleEngine
from app.core.kafka_client import KafkaClient
from app.core.config import Config
from app.core.security import login_required
from app.schemas.vitals import VitalsIngestRequest, VitalsResponse
from app.core.utils import api_response
from pydantic import ValidationError

vitals_bp = Blueprint('vitals', __name__, url_prefix='/vitals')

@vitals_bp.route('', methods=['POST'])
# @login_required() # Devices might authenticate differently
def ingest_vitals():
    try:
        data = request.get_json()
        if not data:
            return api_response(error="No input data provided", status_code=400)
        req = VitalsIngestRequest(**data)
    except ValidationError as e:
        return api_response(error=e.errors(), status_code=400)
    except ValueError as e:
        return api_response(error=str(e), status_code=400)

    db = next(get_db())
    # Convert Pydantic model to dict for repository, handling datetime serialization if needed
    vitals_data = req.model_dump()
    vitals = VitalsRepository.create_vitals(db, vitals_data)
    
    # Publish to Kafka
    vitals_payload = vitals_data.copy()
    vitals_payload['timestamp'] = vitals_payload['timestamp'].isoformat()
    KafkaClient.send_message(Config.KAFKA_TOPIC_VITALS, vitals_payload)
    
    # Rule Engine is now handled by the Alert Engine consumer
    
    return api_response(data={'id': vitals.id, 'status': 'received'}, status_code=201)

@vitals_bp.route('', methods=['GET'])
@login_required()
def get_vitals():
    patient_id = request.args.get('patient_id')
    encounter_id = request.args.get('encounter_id')
    last_minutes = request.args.get('last_minutes')
    
    db = next(get_db())
    vitals_list = VitalsRepository.get_vitals(db, patient_id, encounter_id, last_minutes)
    
    return api_response(data=[VitalsResponse.model_validate(v).model_dump() for v in vitals_list])
