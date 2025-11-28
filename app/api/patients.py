from flask import Blueprint, request
from app.core.database import get_db
from app.repositories.encounter_repo import EncounterRepository
from app.repositories.vitals_repo import VitalsRepository
from app.core.security import login_required
from app.schemas.frontend import PatientEncounterResponse, PatientVitalsResponse, ActiveEncounter, PatientBasicInfo, RoomInfo, VitalsPoint
from app.core.utils import api_response

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

@patients_bp.route('/<int:id>/encounter', methods=['GET'])
@login_required(roles=['patient', 'doctor', 'admin'])
def get_patient_encounter(id):
    # RBAC: Patient can only see their own data
    current_user = request.current_user
    if current_user['role'] == 'patient' and current_user['user_id'] != id:
        return api_response(error="Unauthorized access to another patient's data", status_code=403)

    db = next(get_db())
    encounter = EncounterRepository.get_active_encounter_for_patient(db, id)
    
    if not encounter:
        return api_response(data=PatientEncounterResponse(encounter=None).model_dump())
        
    # Safe access to relationships
    patient = encounter.patient
    room = encounter.room
    
    active_encounter = ActiveEncounter(
        id=encounter.id,
        patient=PatientBasicInfo(
            id=patient.id,
            name=f"Patient {patient.id}",
            age=None,
            gender=patient.gender
        ),
        room=RoomInfo(
            id=room.id,
            room_number=room.room_number
        ),
        admitted_at=encounter.admitted_at,
        status=encounter.status
    )
    
    return api_response(data=PatientEncounterResponse(encounter=active_encounter).model_dump())

@patients_bp.route('/<int:id>/vitals/recent', methods=['GET'])
@login_required(roles=['patient', 'doctor', 'admin'])
def get_patient_vitals(id):
    # RBAC: Patient can only see their own data
    current_user = request.current_user
    if current_user['role'] == 'patient' and current_user['user_id'] != id:
        return api_response(error="Unauthorized access to another patient's data", status_code=403)
        
    limit = request.args.get('limit', 10)
    
    db = next(get_db())
    # We need to find the active encounter first to get relevant vitals, or just get all vitals for patient?
    # The requirement says "last N vitals points". Usually this implies for the current stay or just recent history.
    # I'll fetch by patient_id using the existing repo method which supports filtering.
    
    vitals_list = VitalsRepository.get_vitals(db, patient_id=id)
    # The repo returns all, ordered by desc. I'll slice it here. 
    # Optimization: Repo should support limit. But for now slicing is fine for MVP.
    
    recent_vitals = vitals_list[:int(limit)]
    
    response_data = [
        VitalsPoint(
            timestamp=v.timestamp,
            hr_bpm=v.hr_bpm,
            spo2_pct=v.spo2_pct,
            temp_c=v.temp_c,
            bp_systolic=v.bp_systolic,
            bp_diastolic=v.bp_diastolic,
            resp_rate=v.resp_rate
        ) for v in recent_vitals
    ]
    
    return api_response(data=PatientVitalsResponse(vitals=response_data).model_dump())
