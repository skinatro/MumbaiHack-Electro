from flask import Blueprint, request
from app.core.database import get_db
from app.domain.models import Observation
from app.core.security import login_required
from app.schemas.observations import CreateObservationRequest, ObservationResponse
from app.core.utils import api_response
from pydantic import ValidationError

observations_bp = Blueprint('observations', __name__, url_prefix='/observations')

@observations_bp.route('', methods=['POST'])
@login_required(roles=['doctor', 'nurse'])
def create_observation():
    try:
        data = request.get_json()
        if not data:
            return api_response(error="No input data provided", status_code=400)
        req = CreateObservationRequest(**data)
    except ValidationError as e:
        return api_response(error=e.errors(), status_code=400)

    db = next(get_db())
    
    observation = Observation(
        encounter_id=req.encounter_id,
        author_id=request.current_user['user_id'],
        note=req.note
    )
    db.add(observation)
    db.commit()
    db.refresh(observation)
    
    return api_response(data={'id': observation.id, 'status': 'created'}, status_code=201)

@observations_bp.route('', methods=['GET'])
@login_required()
def get_observations():
    encounter_id = request.args.get('encounter_id')
    db = next(get_db())
    
    query = db.query(Observation)
    if encounter_id:
        query = query.filter(Observation.encounter_id == encounter_id)
        
    observations = query.all()
    return api_response(data=[ObservationResponse.model_validate(o).model_dump() for o in observations])
