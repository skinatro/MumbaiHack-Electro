from flask import Blueprint, request
from app.core.database import get_db
from app.domain.models import Alert
from app.core.security import login_required
from app.core.utils import api_response

alerts_bp = Blueprint('alerts', __name__, url_prefix='/alerts')

@alerts_bp.route('/<int:id>/resolve', methods=['PATCH'])
@login_required(roles=['doctor', 'admin'])
def resolve_alert(id):
    db = next(get_db())
    alert = db.query(Alert).get(id)
    
    if not alert:
        return api_response(error='Alert not found', status_code=404)
        
    alert.resolved = True
    db.commit()
    
    return api_response(data={'id': alert.id, 'status': 'resolved'})
