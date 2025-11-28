from flask import Blueprint, request
from app.core.database import get_db
from app.services.discharge_service import DischargeService
from app.core.security import login_required
from app.domain.models import Encounter, DischargePlan, User

discharge_bp = Blueprint('discharge', __name__)

@discharge_bp.route('/discharge/auto/run', methods=['POST'])
@login_required(roles=['admin', 'doctor'])
def run_auto_discharge():
    """
    Manually triggers the auto-discharge evaluation for all active encounters.
    """
    db = next(get_db())
    encounters = db.query(Encounter).filter(
        Encounter.status == "active",
        Encounter.auto_discharge_blocked == False
    ).all()
    
    results = {
        "evaluated": len(encounters),
        "auto_discharged": [],
        "skipped": [],
        "reasons": {}
    }
    
    for encounter in encounters:
        try:
            if DischargeService.is_stable_for_discharge(encounter.id, db):
                # Discharge
                DischargeService.discharge_encounter(encounter.id, db)
                # Generate Plan
                DischargeService.generate_discharge_plan(encounter.id, db)
                results["auto_discharged"].append(encounter.id)
            else:
                results["skipped"].append(encounter.id)
                results["reasons"][str(encounter.id)] = "Criteria not met (Time/Alerts/Vitals)"
        except Exception as e:
            results["skipped"].append(encounter.id)
            results["reasons"][str(encounter.id)] = f"Error: {str(e)}"
            
    return api_response(data=results)

@discharge_bp.route('/encounters/<int:encounter_id>/discharge_plan', methods=['GET'])
@login_required(roles=['admin', 'doctor', 'patient'])
def get_discharge_plan(encounter_id):
    """
    Fetch the discharge plan for a specific encounter.
    """
    db = next(get_db())
    plan = db.query(DischargePlan).filter(DischargePlan.encounter_id == encounter_id).first()
    
    if not plan:
        return api_response(error="Discharge plan not found", status_code=404)
        
    # Check ownership if patient
    # Check ownership if patient
    current_user_id = request.current_user['user_id']
    current_user_role = request.current_user['role']
    
    if current_user_role == 'patient':
        # Ensure patient owns this encounter
        encounter = db.query(Encounter).filter(Encounter.id == encounter_id).first()
        if not encounter or encounter.patient.user_id != current_user_id:
             return api_response(error="Unauthorized", status_code=403)

    return api_response(data={
        "encounter_id": plan.encounter_id,
        "patient_id": plan.patient_id,
        "summary": plan.summary,
        "home_care_instructions": plan.home_care_instructions, # It's already JSON string if stored as Text, or need parsing?
        # In service we stored it as json.dumps(). So here we should parse it back if we want to return JSON object, 
        # or return as string. API usually returns JSON object.
        # Let's parse it.
        "recommended_meds": plan.recommended_meds,
        "followup_days": plan.followup_days,
        "created_at": plan.created_at
    })

@discharge_bp.route('/patients/me/post_discharge', methods=['GET'])
@login_required(roles=['patient'])
def get_my_post_discharge():
    """
    Fetch the most recent discharge plan for the logged-in patient.
    """
    db = next(get_db())
    current_user_id = request.current_user['user_id']
    current_user = db.query(User).filter(User.id == current_user_id).first()
    
    # Find patient profile
    if not current_user or not current_user.patient_profile:
        return api_response(error="Patient profile not found", status_code=404)
        
    # Find latest discharge plan
    plan = db.query(DischargePlan).filter(
        DischargePlan.patient_id == current_user.patient_profile.id
    ).order_by(DischargePlan.created_at.desc()).first()
    
    if not plan:
        return api_response(error="No discharge plan found", status_code=404)
        
    return api_response(data={
        "encounter_id": plan.encounter_id,
        "summary": plan.summary,
        "home_care_instructions": plan.home_care_instructions,
        "recommended_meds": plan.recommended_meds,
        "followup_days": plan.followup_days
    })
