from flask import Blueprint, jsonify
from app.llm.healthcheck import llm_healthcheck
from app.services.llm_service import LLMService

llm_health_bp = Blueprint('llm_health', __name__)

@llm_health_bp.route('/llm/health', methods=['GET'])
def llm_health():
    """
    Lightweight healthcheck for LangChain + Ollama integration.
    Does a tiny test call and returns status + minimal info.
    """
    result = llm_healthcheck()
    status_code = 200 if result["ok"] else 500

    return jsonify({
        "status": "success" if result["ok"] else "error",
        "data": {
            "model": result["model"],
            "ok": result["ok"],
            "sample_reply": result["sample_reply"],
        },
        "error": result["error"],
    }), status_code

@llm_health_bp.route('/llm/copilot/smoke_test', methods=['GET'])
def copilot_smoke_test():
    """
    Smoke test for the doctor copilot pipeline.
    Uses a fake context to generate an alert explanation.
    """
    fake_context = {
        "alert_type": "tachycardia",
        "severity": "medium",
        "message": "HR 130 bpm earlier today",
        "patient_age": 45,
        "gender": "M",
        "recent_vitals": [
            {"hr": 95, "spo2": 97, "bp": "130/85", "temp": 37.2}
        ]
    }
    
    try:
        # Call the actual service method
        result = LLMService.generate_alert_explanation_json(fake_context)
        
        return jsonify({
            "status": "success",
            "data": {
                "structured_output": result
            },
            "error": None
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "data": None,
            "error": str(e)
        }), 500
