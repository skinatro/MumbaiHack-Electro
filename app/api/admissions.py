from flask import Blueprint, request
from app.core.database import get_db
from app.services.admission_service import AdmissionService
from app.schemas.admission import AdmissionRequest
from app.core.utils import api_response
from app.core.security import login_required
from pydantic import ValidationError

admissions_bp = Blueprint('admissions', __name__, url_prefix='/admissions')

@admissions_bp.route('/auto', methods=['POST'])
@login_required(roles=['admin', 'doctor'])
def auto_admission():
    """
    Auto-admit a patient, allocate room, and create an encounter using simple triage rules.
    """
    try:
        data = request.get_json()
        if not data:
            return api_response(error="No input data provided", status_code=400)
            
        payload = AdmissionRequest(**data)
        db = next(get_db())
        
        result = AdmissionService.auto_admit(payload, db)
        
        return api_response(data=result.model_dump(), status_code=201)
        
    except ValidationError as e:
        return api_response(error=e.errors(), status_code=400)
    except ValueError as e:
        return api_response(error=str(e), status_code=409) # Conflict/Resource Exhausted
    except Exception as e:
        import traceback
        traceback.print_exc()
        return api_response(error=str(e), status_code=500)
