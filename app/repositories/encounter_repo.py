from sqlalchemy.orm import Session
from app.domain.models import Encounter, Room, Patient
from datetime import datetime

class EncounterRepository:
    @staticmethod
    def get_available_room(db: Session):
        return db.query(Room).filter(Room.is_occupied == False).first()

    @staticmethod
    def admit_patient(db: Session, patient_id, doctor_id, room_id):
        # Mark room as occupied
        room = db.query(Room).get(room_id)
        room.is_occupied = True
        
        encounter = Encounter(
            patient_id=patient_id,
            doctor_id=doctor_id,
            room_id=room_id,
            status='active'
        )
        db.add(encounter)
        db.commit()
        db.refresh(encounter)
        return encounter

    @staticmethod
    def get_encounter(db: Session, encounter_id):
        return db.query(Encounter).get(encounter_id)
