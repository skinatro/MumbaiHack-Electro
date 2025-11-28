import unittest
from unittest.mock import MagicMock, patch
from app.services.alert_copilot import AlertCopilotService
from app.domain.models import Alert, AlertExplanation, Patient, Vitals
from datetime import datetime

class TestAlertCopilotService(unittest.TestCase):
    @patch('app.services.alert_copilot.KafkaConsumer')
    @patch('app.services.alert_copilot.SessionLocal')
    @patch('app.services.alert_copilot.LLMService')
    def test_process_alert(self, mock_llm, mock_session_cls, mock_kafka):
        # Setup mocks
        mock_db = MagicMock()
        mock_session_cls.return_value = mock_db
        
        # Mock Alert
        mock_alert = MagicMock()
        mock_alert.id = 1
        mock_alert.type = "tachycardia"
        mock_alert.severity = "high"
        mock_alert.message = "HR > 100"
        mock_alert.patient_id = 1
        mock_alert.encounter_id = 1
        mock_alert.explanation = None # No existing explanation
        
        mock_db.query.return_value.filter.return_value.first.side_effect = [
            mock_alert, # First call for Alert
            MagicMock(dob=datetime(1980, 1, 1), gender="Male") # Second call for Patient
        ]
        
        # Mock Vitals
        mock_db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []
        
        # Mock LLM
        mock_llm.generate_alert_explanation_json.return_value = {
            "summary": "Summary",
            "risk_level": "High",
            "suggested_checks": ["Check 1"],
            "suggested_actions": ["Action 1"]
        }
        
        # Run process_alert
        service = AlertCopilotService()
        service.process_alert({"id": 1, "type": "tachycardia"})
        
        # Verify DB add was called (saving explanation)
        mock_db.add.assert_called()
        args, _ = mock_db.add.call_args
        explanation = args[0]
        self.assertIsInstance(explanation, AlertExplanation)
        self.assertEqual(explanation.alert_id, 1)
        self.assertEqual(explanation.summary, "Summary")
        self.assertEqual(explanation.risk_level, "High")

if __name__ == '__main__':
    unittest.main()
