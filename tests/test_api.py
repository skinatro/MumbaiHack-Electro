import unittest
from unittest.mock import MagicMock, patch
from app.app import create_app
from app.schemas.auth import LoginRequest
import json

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.api.auth.UserRepository')
    @patch('app.api.auth.verify_password')
    @patch('app.api.auth.create_access_token')
    @patch('app.api.auth.get_db')
    def test_login_success(self, mock_get_db, mock_create_token, mock_verify, mock_repo):
        mock_user = MagicMock()
        mock_user.username = 'testuser'
        mock_user.password_hash = 'hashed'
        mock_user.role = 'doctor'
        mock_user.id = 1
        
        mock_repo.get_by_username.return_value = mock_user
        mock_verify.return_value = True
        mock_create_token.return_value = 'fake-token'
        
        response = self.client.post('/auth/login', json={'username': 'testuser', 'password': 'password'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['access_token'], 'fake-token')

    def test_login_validation_error(self):
        response = self.client.post('/auth/login', json={'username': ''}) # Missing password
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('error', data)

    @patch('app.api.vitals.VitalsRepository')
    @patch('app.api.vitals.KafkaClient')
    @patch('app.api.vitals.RuleEngine')
    @patch('app.api.vitals.get_db')
    def test_ingest_vitals_success(self, mock_get_db, mock_rule, mock_kafka, mock_repo):
        mock_vitals = MagicMock()
        mock_vitals.id = 123
        mock_repo.create_vitals.return_value = mock_vitals
        mock_rule.evaluate.return_value = []
        
        payload = {
            "patient_id": 1,
            "encounter_id": 10,
            "timestamp": "2023-10-27T10:00:00Z",
            "hr_bpm": 80,
            "spo2_pct": 98,
            "temp_c": 37.0
        }
        
        response = self.client.post('/vitals', json=payload)
        
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['id'], 123)

    def test_ingest_vitals_validation_error(self):
        payload = {
            "patient_id": 1,
            # Missing encounter_id
            "timestamp": "2023-10-27T10:00:00Z"
        }
        response = self.client.post('/vitals', json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
