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

from app.services.alert_service import AlertService

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
    
    # Publish to Kafka (Vitals Stream)
    vitals_payload = vitals_data.copy()
    vitals_payload['timestamp'] = vitals_payload['timestamp'].isoformat()
    KafkaClient.send_message(Config.KAFKA_TOPIC_VITALS, vitals_payload)
    
    # Synchronous Alert Evaluation
    alerts_triggered = AlertService.evaluate_vitals(db, vitals)
    
    return api_response(data={'id': vitals.id, 'status': 'received', 'alerts': alerts_triggered}, status_code=201)

@vitals_bp.route('', methods=['GET'])
@login_required()
def get_vitals():
    patient_id = request.args.get('patient_id')
    encounter_id = request.args.get('encounter_id')
    last_minutes = request.args.get('last_minutes')
    
    current_user = request.current_user
    
    # RBAC: Patient can only see their own vitals
    if current_user['role'] == 'patient':
        # If patient_id is provided, it must match
        if patient_id and int(patient_id) != current_user['user_id']: # Wait, patient_id is Patient ID, not User ID.
             # We need to resolve Patient ID from User ID.
             # This is tricky without querying DB.
             # Let's assume we can get patient profile from DB.
             pass # Logic below
             
    db = next(get_db())
    
    # Resolve Patient ID for RBAC
    if current_user['role'] == 'patient':
        from app.domain.models import Patient
        patient_profile = db.query(Patient).filter(Patient.user_id == current_user['user_id']).first()
        if not patient_profile:
            return api_response(error="Patient profile not found", status_code=404)
            
        # Enforce filtering by this patient
        if patient_id and int(patient_id) != patient_profile.id:
            return api_response(error="Unauthorized", status_code=403)
            
        # If no patient_id provided, force it
        patient_id = patient_profile.id
        
    vitals_list = VitalsRepository.get_vitals(db, patient_id, encounter_id, last_minutes)
    
    return api_response(data=[VitalsResponse.model_validate(v).model_dump() for v in vitals_list])
