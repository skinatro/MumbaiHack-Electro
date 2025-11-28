import unittest
from unittest.mock import MagicMock, patch
from app.services.admission_service import AdmissionService
from app.schemas.admission import AdmissionRequest
from app.domain.models import Room, User, Patient, Encounter, Doctor
from datetime import datetime

class TestAdmissionService(unittest.TestCase):
    def test_decide_department_icu(self):
        req = AdmissionRequest(
            name="Test", age=50, symptoms=["chest pain"], complaint_description="Severe pain"
        )
        dept = AdmissionService.decide_department(req)
        self.assertEqual(dept, "ICU")

    def test_decide_department_general(self):
        req = AdmissionRequest(
            name="Test", age=50, symptoms=["cough"], complaint_description="Mild cough"
        )
        dept = AdmissionService.decide_department(req)
        self.assertEqual(dept, "General")

    def test_allocate_room_success(self):
        db = MagicMock()
        mock_room = MagicMock()
        mock_room.room_number = "101"
        mock_room.department = "ICU"
        
        db.query.return_value.filter.return_value.order_by.return_value.first.return_value = mock_room
        
        room = AdmissionService.allocate_room("ICU", db)
        self.assertEqual(room.room_number, "101")

    def test_allocate_room_fallback(self):
        db = MagicMock()
        
        # First query (ICU) returns None
        # Second query (General) returns Room
        mock_room_gen = MagicMock()
        mock_room_gen.room_number = "201"
        mock_room_gen.department = "General"
        
        # Mocking the chain is tricky with multiple calls. 
        # Using side_effect for first()
        
        query_mock = db.query.return_value
        filter_mock = query_mock.filter.return_value
        order_mock = filter_mock.order_by.return_value
        
        # First call returns None, Second call returns Room
        order_mock.first.side_effect = [None, mock_room_gen]
        
        room = AdmissionService.allocate_room("ICU", db)
        self.assertEqual(room.room_number, "201")
        self.assertEqual(room.department, "General")

if __name__ == '__main__':
    unittest.main()
