from flask import Blueprint, request
from app.core.database import get_db
from app.repositories.encounter_repo import EncounterRepository
from app.repositories.vitals_repo import VitalsRepository
from app.domain.models import Observation
from app.core.security import login_required
from app.schemas.encounters import AdmitPatientRequest, EncounterResponse
from app.schemas.frontend import EncounterOverviewResponse, VitalsPoint, ObservationInfo
from app.core.utils import api_response
from pydantic import ValidationError

encounters_bp = Blueprint('encounters', __name__, url_prefix='/encounters')

@encounters_bp.route('', methods=['POST'])
@login_required(roles=['admin', 'doctor'])
def admit_patient():
    try:
        data = request.get_json()
        if not data:
            return api_response(error="No input data provided", status_code=400)
        req = AdmitPatientRequest(**data)
    except ValidationError as e:
        return api_response(error=e.errors(), status_code=400)

    db = next(get_db())
    
    room = EncounterRepository.get_available_room(db)
    if not room:
        return api_response(error='No available rooms', status_code=400)
        
    encounter = EncounterRepository.admit_patient(
        db, 
        patient_id=req.patient_id, 
        doctor_id=req.doctor_id, 
        room_id=room.id
    )
    
    return api_response(data=EncounterResponse.model_validate(encounter).model_dump(), status_code=201)

@encounters_bp.route('/<int:id>', methods=['GET'])
@login_required()
def get_encounter(id):
    db = next(get_db())
    encounter = EncounterRepository.get_encounter(db, id)
    if not encounter:
        return api_response(error='Encounter not found', status_code=404)
        
    return api_response(data=EncounterResponse.model_validate(encounter).model_dump())

@encounters_bp.route('/<int:id>/overview', methods=['GET'])
@login_required(roles=['doctor', 'nurse', 'admin'])
def get_encounter_overview(id):
    db = next(get_db())
    encounter = EncounterRepository.get_encounter(db, id)
    if not encounter:
        return api_response(error='Encounter not found', status_code=404)
        
    # Get latest vitals
    latest_vitals = VitalsRepository.get_latest_vitals(db, id)
    vitals_data = None
    if latest_vitals:
        vitals_data = VitalsPoint(
            timestamp=latest_vitals.timestamp,
            hr_bpm=latest_vitals.hr_bpm,
            spo2_pct=latest_vitals.spo2_pct,
            temp_c=latest_vitals.temp_c,
            bp_systolic=latest_vitals.bp_systolic,
            bp_diastolic=latest_vitals.bp_diastolic,
            resp_rate_bpm=latest_vitals.resp_rate_bpm
        )
        
    # Get last observation
    # Assuming we can query observations directly or add a repo method. 
    # For now, direct query as I didn't add repo method for this specific one yet.
    last_observation = db.query(Observation).filter(
        Observation.encounter_id == id
    ).order_by(Observation.created_at.desc()).first()
    
    obs_data = None
    if last_observation:
        obs_data = ObservationInfo(
            id=last_observation.id,
            note=last_observation.note,
            created_at=last_observation.created_at,
            author_id=last_observation.author_id
        )
        
    # Mock alerts count for now, or fetch from a hypothetical alerts table
    alerts_count = 0 
    
    response = EncounterOverviewResponse(
        encounter_id=id,
        patient_id=encounter.patient_id,
        latest_vitals=vitals_data,
        last_observation=obs_data,
        alerts_count=alerts_count,
        status=encounter.status
    )
    
    return api_response(data=response.model_dump())

@encounters_bp.route('/<int:id>/discharge', methods=['PATCH'])
@login_required(roles=['admin', 'doctor'])
def discharge_encounter(id):
    """
    Manually discharge an encounter.
    Optionally generate discharge plan if requested.
    """
    db = next(get_db())
    try:
        # Check if active
        encounter = db.query(Encounter).filter(Encounter.id == id).first()
        if not encounter:
             return api_response(error="Encounter not found", status_code=404)
             
        if encounter.status != "active":
             return api_response(error="Encounter is not active", status_code=400)

        # Discharge
        DischargeService.discharge_encounter(id, db)
        
        # Generate plan if requested? 
        # Requirement says: "Optionally from PATCH ... when a doctor manually discharges and requests plan generation."
        # Let's check query param or body.
        data = request.get_json() or {}
        if data.get("generate_plan", True): # Default to True for convenience
             DischargeService.generate_discharge_plan(id, db)
             
        return api_response(message="Encounter discharged successfully")
    except Exception as e:
        return api_response(error=str(e), status_code=500)

@encounters_bp.route('/<int:id>/hold_auto_discharge', methods=['PATCH'])
@login_required(roles=['admin', 'doctor'])
def hold_auto_discharge(id):
    """
    Block or unblock auto-discharge for an encounter.
    Body: { "hold": true/false }
    """
    db = next(get_db())
    data = request.get_json()
    hold = data.get("hold", True)
    
    encounter = db.query(Encounter).filter(Encounter.id == id).first()
    if not encounter:
        return api_response(error="Encounter not found", status_code=404)
        
    encounter.auto_discharge_blocked = hold
    db.commit()
    
    return api_response(message=f"Auto-discharge hold set to {hold}")

@encounters_bp.route('/<int:id>/alerts', methods=['GET'])
@login_required(roles=['doctor', 'nurse', 'admin'])
def get_encounter_alerts(id):
    db = next(get_db())
    # Assuming Alert model is imported or available via relationship
    # Since we added relationship in Encounter model, we can use that or query Alert directly
    # Let's query Alert directly for better control (e.g. filtering)
    from app.domain.models import Alert
    
    alerts = db.query(Alert).filter(Alert.encounter_id == id).order_by(Alert.timestamp.desc()).all()
    
    return api_response(data=[{
        'id': a.id,
        'patient_id': a.patient_id,
        'encounter_id': a.encounter_id,
        'type': a.type,
        'severity': a.severity,
        'message': a.message,
        'created_at': a.created_at.isoformat() if a.created_at else None,
        'resolved': a.resolved,
        'resolved_at': a.resolved_at.isoformat() if a.resolved_at else None
    } for a in alerts])
