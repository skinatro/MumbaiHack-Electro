from sqlalchemy.orm import Session
from app.domain.models import Encounter, Room, Patient, User
from datetime import datetime

class EncounterRepository:
    """
    Repository for Encounter and Room entities.
    Handles patient admission and encounter management.
    """
    @staticmethod
    def get_available_room(db: Session):
        """Find the first available room."""
        return db.query(Room).filter(Room.is_occupied == False).first()

    @staticmethod
    def admit_patient(db: Session, patient_id, doctor_id, room_id):
        """
        Admit a patient to a room.
        Marks the room as occupied and creates an active encounter.
        """
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
        """Retrieve an encounter by ID."""
        return db.query(Encounter).get(encounter_id)

    @staticmethod
    def get_active_encounters_for_doctor(db: Session, doctor_id: int):
        """Get all active encounters for a specific doctor."""
        return db.query(Encounter).filter(
            Encounter.doctor_id == doctor_id,
            Encounter.status == 'active'
        ).all()

    @staticmethod
    def get_active_encounter_for_patient(db: Session, patient_id: int):
        """Get the current active encounter for a patient."""
        return db.query(Encounter).filter(
            Encounter.patient_id == patient_id,
            Encounter.status == 'active'
        ).first()
