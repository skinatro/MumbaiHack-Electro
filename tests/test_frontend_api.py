import unittest
from unittest.mock import MagicMock, patch
from app.app import create_app
from datetime import datetime

class TestFrontendAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    @patch('app.core.security.decode_access_token')
    @patch('app.api.doctors.EncounterRepository')
    @patch('app.api.doctors.get_db')
    def test_get_doctor_patients_success(self, mock_get_db, mock_repo, mock_decode):
        # Mock Auth
        mock_decode.return_value = {'sub': 'doc1', 'role': 'doctor', 'user_id': 10}
        
        # Mock Data
        mock_enc = MagicMock()
        mock_enc.id = 101
        mock_enc.patient.id = 1
        mock_enc.patient.gender = 'M'
        mock_enc.room.id = 5
        mock_enc.room.room_number = '101A'
        mock_enc.admitted_at = datetime(2023, 10, 27, 10, 0, 0)
        mock_enc.status = 'active'
        
        mock_repo.get_active_encounters_for_doctor.return_value = [mock_enc]
        
        # Request
        response = self.client.get('/doctors/10/patients', headers={'Authorization': 'Bearer fake-token'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(len(data['data']['encounters']), 1)
        self.assertEqual(data['data']['encounters'][0]['id'], 101)

    @patch('app.core.security.decode_access_token')
    def test_get_doctor_patients_rbac_fail(self, mock_decode):
        # Mock Auth as different doctor
        mock_decode.return_value = {'sub': 'doc2', 'role': 'doctor', 'user_id': 99}
        
        # Request for doctor 10
        response = self.client.get('/doctors/10/patients', headers={'Authorization': 'Bearer fake-token'})
        
        self.assertEqual(response.status_code, 403)

    @patch('app.core.security.decode_access_token')
    @patch('app.api.patients.EncounterRepository')
    @patch('app.api.patients.get_db')
    def test_get_patient_encounter_success(self, mock_get_db, mock_repo, mock_decode):
        # Mock Auth
        mock_decode.return_value = {'sub': 'pat1', 'role': 'patient', 'user_id': 1}
        
        # Mock Data
        mock_enc = MagicMock()
        mock_enc.id = 101
        mock_enc.patient.id = 1
        mock_enc.patient.gender = 'M'
        mock_enc.room.id = 5
        mock_enc.room.room_number = '101A'
        mock_enc.admitted_at = datetime(2023, 10, 27, 10, 0, 0)
        mock_enc.status = 'active'
        
        mock_repo.get_active_encounter_for_patient.return_value = mock_enc
        
        # Request
        response = self.client.get('/patients/1/encounter', headers={'Authorization': 'Bearer fake-token'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['encounter']['id'], 101)

    @patch('app.core.security.decode_access_token')
    def test_get_patient_encounter_rbac_fail(self, mock_decode):
        # Mock Auth as different patient
        mock_decode.return_value = {'sub': 'pat2', 'role': 'patient', 'user_id': 2}
        
        # Request for patient 1
        response = self.client.get('/patients/1/encounter', headers={'Authorization': 'Bearer fake-token'})
        
        self.assertEqual(response.status_code, 403)

    @patch('app.core.security.decode_access_token')
    @patch('app.api.encounters.EncounterRepository')
    @patch('app.api.encounters.VitalsRepository')
    @patch('app.api.encounters.get_db')
    def test_get_encounter_overview_success(self, mock_get_db, mock_vitals_repo, mock_enc_repo, mock_decode):
        # Mock Auth
        mock_decode.return_value = {'sub': 'doc1', 'role': 'doctor', 'user_id': 10}
        
        # Mock DB Session
        mock_db = MagicMock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock Encounter
        mock_enc = MagicMock()
        mock_enc.id = 101
        mock_enc.patient_id = 1
        mock_enc.status = 'active'
        mock_enc_repo.get_encounter.return_value = mock_enc
        
        # Mock Vitals
        mock_vitals = MagicMock()
        mock_vitals.timestamp = datetime(2023, 10, 27, 10, 5, 0)
        mock_vitals.hr_bpm = 80
        mock_vitals.spo2_pct = 98.0
        mock_vitals.temp_c = 37.0
        mock_vitals.bp_systolic = 120
        mock_vitals.bp_diastolic = 80
        mock_vitals.resp_rate = 16
        mock_vitals_repo.get_latest_vitals.return_value = mock_vitals
        
        # Mock Observation Query
        # db.query(Observation).filter(...).order_by(...).first()
        mock_obs = MagicMock()
        mock_obs.id = 50
        mock_obs.note = "Patient resting"
        mock_obs.created_at = datetime(2023, 10, 27, 9, 0, 0)
        mock_obs.author_id = 2
        
        # Chain the mocks
        mock_db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_obs
        
        # Request
        response = self.client.get('/encounters/101/overview', headers={'Authorization': 'Bearer fake-token'})
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['data']['latest_vitals']['hr_bpm'], 80)

if __name__ == '__main__':
    unittest.main()
