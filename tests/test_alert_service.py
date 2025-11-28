import unittest
from unittest.mock import MagicMock, patch
from app.services.alert_service import AlertService
from app.app import create_app
from datetime import datetime

class TestAlertService(unittest.TestCase):
    def test_evaluate_vitals_tachycardia(self):
        db = MagicMock()
        vitals = MagicMock()
        vitals.hr_bpm = 140
        vitals.spo2_pct = 98
        vitals.temp_c = 37.0
        vitals.bp_systolic = 120
        vitals.bp_diastolic = 80
        vitals.patient_id = 1
        vitals.encounter_id = 10
        vitals.timestamp = datetime.now()
        
        alerts = AlertService.evaluate_vitals(db, vitals)
        self.assertIn('tachycardia', alerts)
        # Verify db.add was called
        self.assertTrue(db.add.called)
        # Verify Kafka publish (mocked inside)

    def test_evaluate_vitals_normal(self):
        db = MagicMock()
        vitals = MagicMock()
        vitals.hr_bpm = 80
        vitals.spo2_pct = 98
        vitals.temp_c = 37.0
        vitals.bp_systolic = 120
        vitals.bp_diastolic = 80
        
        alerts = AlertService.evaluate_vitals(db, vitals)
        self.assertEqual(len(alerts), 0)
        self.assertFalse(db.add.called)

class TestAlertAPIIntegration(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.core.security.decode_access_token')
    @patch('app.api.doctors.get_db')
    def test_get_recent_alerts(self, mock_get_db, mock_decode):
        mock_decode.return_value = {'sub': 'doc1', 'role': 'doctor', 'user_id': 10}
        
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])
        
        mock_doc = MagicMock()
        mock_doc.id = 5
        mock_db.query.return_value.filter.return_value.first.return_value = mock_doc
        
        mock_alert = MagicMock()
        mock_alert.id = 1
        mock_alert.patient_id = 100
        mock_alert.encounter_id = 200
        mock_alert.severity = 'high'
        mock_alert.type = 'tachycardia'
        mock_alert.message = 'HR 140'
        mock_alert.created_at = datetime(2023, 10, 27, 10, 0, 0)
        
        mock_db.query.return_value.join.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = [mock_alert]
        
        response = self.client.get('/doctors/me/alerts/recent', headers={'Authorization': 'Bearer fake-token'})
        if response.status_code != 200:
            print(f"Response: {response.get_json()}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['type'], 'tachycardia')

if __name__ == '__main__':
    unittest.main()
