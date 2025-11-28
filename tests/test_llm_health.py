import unittest
from unittest.mock import MagicMock, patch
from app.llm.healthcheck import llm_healthcheck
from app.services.llm_service import LLMService
import json

class TestLLMHealthcheck(unittest.TestCase):
    @patch('app.llm.healthcheck.get_default_llm')
    def test_llm_healthcheck_success(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.return_value.content = "OK"
        mock_llm.model = "llama3"
        mock_get_llm.return_value = mock_llm
        
        result = llm_healthcheck()
        self.assertTrue(result["ok"])
        self.assertEqual(result["model"], "llama3")
        self.assertEqual(result["sample_reply"], "OK")

    @patch('app.llm.healthcheck.get_default_llm')
    def test_llm_healthcheck_failure(self, mock_get_llm):
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("Connection refused")
        mock_llm.model = "llama3"
        mock_get_llm.return_value = mock_llm
        
        result = llm_healthcheck()
        self.assertFalse(result["ok"])
        self.assertIn("Connection refused", result["error"])

    @patch('app.services.llm_service.get_default_llm')
    def test_llm_service_fallback(self, mock_get_llm):
        # Test fallback when LLM fails
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("LLM Error")
        mock_get_llm.return_value = mock_llm
        
        result = LLMService.generate_discharge_plan_json({})
        self.assertEqual(result["discharge_summary"], "Error generating plan. Please review manually.")

if __name__ == '__main__':
    unittest.main()
