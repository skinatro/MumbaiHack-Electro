from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.repositories.encounter_repo import EncounterRepository
from app.core.security import login_required

encounters_bp = Blueprint('encounters', __name__, url_prefix='/encounters')

@encounters_bp.route('', methods=['POST'])
@login_required(roles=['admin', 'doctor'])
def admit_patient():
    data = request.get_json()
    db = next(get_db())
    
    room = EncounterRepository.get_available_room(db)
    if not room:
        return jsonify({'error': 'No available rooms'}), 400
        
    encounter = EncounterRepository.admit_patient(
        db, 
        patient_id=data['patient_id'], 
        doctor_id=data['doctor_id'], 
        room_id=room.id
    )
    
    return jsonify({'id': encounter.id, 'room_number': room.room_number, 'status': 'admitted'}), 201

@encounters_bp.route('/<int:id>', methods=['GET'])
@login_required()
def get_encounter(id):
    db = next(get_db())
    encounter = EncounterRepository.get_encounter(db, id)
    if not encounter:
        return jsonify({'error': 'Encounter not found'}), 404
        
    return jsonify({
        'id': encounter.id,
        'patient_id': encounter.patient_id,
        'doctor_id': encounter.doctor_id,
        'room_id': encounter.room_id,
        'status': encounter.status,
        'admitted_at': encounter.admitted_at.isoformat() if encounter.admitted_at else None
    })
