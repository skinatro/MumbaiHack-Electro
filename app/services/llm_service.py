from app.llm.client import get_default_llm
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import logging
import json

logger = logging.getLogger(__name__)

class LLMService:
    @staticmethod
    def generate_discharge_plan_json(context: dict) -> dict:
        """
        Generates a structured discharge plan using an LLM.
        """
        logger.info(f"Generating discharge plan for context: {context}")
        
        try:
            llm = get_default_llm()
            parser = JsonOutputParser()
            
            prompt = PromptTemplate(
                template="""You are a medical assistant. Generate a discharge plan for a patient based on the following context:
                {context}
                
                Return the output as a JSON object with the following keys:
                - discharge_summary: A short plain-language summary.
                - home_care_instructions: A list of instructions.
                - recommended_meds: A list of objects with "name", "dose", "duration".
                - followup_days: Integer number of days for follow-up.
                
                {format_instructions}
                """,
                input_variables=["context"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            
            chain = prompt | llm | parser
            return chain.invoke({"context": json.dumps(context)})
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            # Fallback to mock if LLM fails (e.g. connection error)
            return {
                "discharge_summary": "Error generating plan. Please review manually.",
                "home_care_instructions": ["Follow standard discharge procedures."],
                "recommended_meds": [],
                "followup_days": 7
            }

    @staticmethod
    def generate_alert_explanation_json(context: dict) -> dict:
        """
        Generates a structured explanation for an alert.
        """
        logger.info(f"Generating alert explanation for context: {context}")
        
        try:
            llm = get_default_llm()
            parser = JsonOutputParser()
            
            prompt = PromptTemplate(
                template="""You are a medical assistant. Analyze the following alert and patient context:
                {context}
                
                Return the output as a JSON object with the following keys:
                - summary: A short summary of the situation.
                - risk_level: "High", "Moderate", or "Low".
                - suggested_checks: A list of things to check.
                - suggested_actions: A list of immediate actions.
                
                {format_instructions}
                """,
                input_variables=["context"],
                partial_variables={"format_instructions": parser.get_format_instructions()}
            )
            
            chain = prompt | llm | parser
            return chain.invoke({"context": json.dumps(context)})
            
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            # Fallback
            return {
                "summary": "Error analyzing alert. Please check vitals manually.",
                "risk_level": "Unknown",
                "suggested_checks": ["Check patient status manually"],
                "suggested_actions": ["Verify alert validity"]
            }
