import json
import logging

logger = logging.getLogger(__name__)

class LLMService:
    @staticmethod
    def generate_discharge_plan_json(context: dict) -> dict:
        """
        Generates a structured discharge plan using an LLM (Mocked for now).
        In a real scenario, this would call OpenAI/Ollama with the context.
        """
        logger.info(f"Generating discharge plan for context: {context}")
        
        # Mock response
        # In production, use LangChain or direct API call here.
        
        patient_age = context.get("patient_age", "unknown")
        condition = "General Recovery"
        
        # Simple logic to make the mock look dynamic
        if "chest pain" in str(context).lower():
            condition = "Cardiac Event"
        
        return {
            "discharge_summary": f"Patient is stable and fit for discharge after {condition}. Vitals are within normal limits.",
            "home_care_instructions": [
                "Rest for 2 days.",
                "Avoid strenuous activity.",
                "Monitor blood pressure daily."
            ],
            "recommended_meds": [
                {
                    "name": "Paracetamol",
                    "dose": "500mg as needed for pain",
                    "duration": "5 days"
                }
            ],
            "followup_days": 7
        }
