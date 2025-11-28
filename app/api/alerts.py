from flask import Blueprint, request
from app.core.database import get_db
from app.domain.models import Alert
from app.core.security import login_required
from app.core.utils import api_response
from datetime import datetime

alerts_bp = Blueprint('alerts', __name__, url_prefix='/alerts')

@alerts_bp.route('/<int:id>/resolve', methods=['PATCH'])
@login_required(roles=['doctor', 'admin'])
def resolve_alert(id):
    db = next(get_db())
    alert = db.query(Alert).filter(Alert.id == id).first()
    
    if not alert:
        return api_response(error='Alert not found', status_code=404)
        
    alert.resolved = True
    alert.resolved_at = datetime.utcnow()
    db.commit()
    
    return api_response(message="Alert resolved")

@alerts_bp.route('/<int:id>/explanation', methods=['GET'])
@login_required(roles=['doctor', 'admin'])
def get_alert_explanation(id):
    """
    Fetch the LLM-generated explanation for an alert.
    """
    db = next(get_db())
    alert = db.query(Alert).filter(Alert.id == id).first()
    if not alert:
        return api_response(error="Alert not found", status_code=404)
        
    explanation = alert.explanation
    if not explanation:
        return api_response(error="Explanation not available yet", status_code=404)
        
    return api_response(data={
        "alert_id": explanation.alert_id,
        "summary": explanation.summary,
        "risk_level": explanation.risk_level,
        "suggested_checks": json.loads(explanation.suggested_checks) if explanation.suggested_checks else [],
        "suggested_actions": json.loads(explanation.suggested_actions) if explanation.suggested_actions else [],
        "created_at": explanation.created_at
    })
