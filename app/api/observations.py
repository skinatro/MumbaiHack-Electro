from flask import Blueprint, request, jsonify
from app.core.database import get_db
from app.domain.models import Observation
from app.core.security import login_required

observations_bp = Blueprint('observations', __name__, url_prefix='/observations')

@observations_bp.route('', methods=['POST'])
@login_required(roles=['doctor', 'nurse']) # Assuming nurse is a role, or just doctor for now
def create_observation():
    data = request.get_json()
    db = next(get_db())
    
    observation = Observation(
        encounter_id=data['encounter_id'],
        author_id=request.current_user['user_id'],
        note=data['note']
    )
    db.add(observation)
    db.commit()
    db.refresh(observation)
    
    return jsonify({'id': observation.id, 'status': 'created'}), 201

@observations_bp.route('', methods=['GET'])
@login_required()
def get_observations():
    encounter_id = request.args.get('encounter_id')
    db = next(get_db())
    
    query = db.query(Observation)
    if encounter_id:
        query = query.filter(Observation.encounter_id == encounter_id)
        
    observations = query.all()
    return jsonify([{
        'id': o.id,
        'author_id': o.author_id,
        'note': o.note,
        'created_at': o.created_at.isoformat()
    } for o in observations])
