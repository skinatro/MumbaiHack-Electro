import unittest
from unittest.mock import MagicMock, patch
from app.services.rule_engine import RuleEngine
from app.app import create_app
from datetime import datetime

class TestAlertEngine(unittest.TestCase):
    def test_rule_engine_tachycardia(self):
        vitals = {'hr_bpm': 140, 'patient_id': 1, 'timestamp': '2023-10-27T10:00:00'}
        alerts = RuleEngine.evaluate(vitals)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'TACHYCARDIA')
        self.assertEqual(alerts[0]['severity'], 'high')

    def test_rule_engine_hypoxia(self):
        vitals = {'spo2_pct': 85, 'patient_id': 1, 'timestamp': '2023-10-27T10:00:00'}
        alerts = RuleEngine.evaluate(vitals)
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'HYPOXIA')

    def test_rule_engine_normal(self):
        vitals = {'hr_bpm': 80, 'spo2_pct': 98, 'temp_c': 37.0, 'patient_id': 1, 'timestamp': '2023-10-27T10:00:00'}
        alerts = RuleEngine.evaluate(vitals)
        self.assertEqual(len(alerts), 0)

class TestAlertAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.core.security.decode_access_token')
    @patch('app.api.encounters.get_db')
    def test_get_encounter_alerts(self, mock_get_db, mock_decode):
        mock_decode.return_value = {'sub': 'doc1', 'role': 'doctor', 'user_id': 10}
        
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])
        
        mock_alert = MagicMock()
        mock_alert.id = 1
        mock_alert.type = 'TACHYCARDIA'
        mock_alert.severity = 'high'
        mock_alert.details = 'High Heart Rate'
        mock_alert.resolved = False
        mock_alert.timestamp = datetime(2023, 10, 27, 10, 0, 0)
        
        mock_db.query.return_value.filter.return_value.order_by.return_value.all.return_value = [mock_alert]
        
        response = self.client.get('/encounters/101/alerts', headers={'Authorization': 'Bearer fake-token'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['type'], 'TACHYCARDIA')

    @patch('app.core.security.decode_access_token')
    @patch('app.api.alerts.get_db')
    def test_resolve_alert(self, mock_get_db, mock_decode):
        mock_decode.return_value = {'sub': 'doc1', 'role': 'doctor', 'user_id': 10}
        
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])
        
        mock_alert = MagicMock()
        mock_alert.id = 1
        mock_alert.resolved = False
        
        mock_db.query.return_value.get.return_value = mock_alert
        
        response = self.client.patch('/alerts/1/resolve', headers={'Authorization': 'Bearer fake-token'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data := response.get_json(), {'status': 'success', 'data': {'id': 1, 'status': 'resolved'}})
        self.assertTrue(mock_alert.resolved)

if __name__ == '__main__':
    unittest.main()
