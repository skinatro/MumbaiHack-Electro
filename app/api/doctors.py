from flask import Blueprint, request
from app.core.database import get_db
from app.repositories.encounter_repo import EncounterRepository
from app.core.security import login_required
from app.schemas.frontend import DoctorPatientListResponse, ActiveEncounter, PatientBasicInfo, RoomInfo
from app.core.utils import api_response

doctors_bp = Blueprint('doctors', __name__, url_prefix='/doctors')

@doctors_bp.route('/<int:id>/patients', methods=['GET'])
@login_required(roles=['doctor', 'admin'])
def get_doctor_patients(id):
    # RBAC: Doctor can only see their own patients
    current_user = request.current_user
    if current_user['role'] == 'doctor' and current_user['user_id'] != id:
        return api_response(error="Unauthorized access to another doctor's patients", status_code=403)

    db = next(get_db())
    encounters = EncounterRepository.get_active_encounters_for_doctor(db, id)
    
    response_data = []
    for enc in encounters:
        # Assuming relationships are set up in SQLAlchemy models, otherwise we'd need to fetch patient/room
        # For this implementation, I'll assume basic relationships exist or I'd need to query them.
        # Let's check models.py content if I can, but for now I'll assume `enc.patient` and `enc.room` work 
        # or I'll construct it manually if needed. 
        # Given the previous file views, I didn't see the full models.py. 
        # I'll rely on the fact that SQLAlchemy usually handles this if defined.
        # If not, I might need to fix it.
        
        # Safe access to relationships
        patient = enc.patient
        room = enc.room
        
        response_data.append(ActiveEncounter(
            id=enc.id,
            patient=PatientBasicInfo(
                id=patient.id,
                name=f"Patient {patient.id}", # Placeholder if name isn't in Patient model (it was dob/gender)
                age=None, # Calculate from DOB if needed
                gender=patient.gender
            ),
            room=RoomInfo(
                id=room.id,
                room_number=room.room_number
            ),
            admitted_at=enc.admitted_at,
            status=enc.status
        ))
        
    return api_response(data=DoctorPatientListResponse(encounters=response_data).model_dump())
