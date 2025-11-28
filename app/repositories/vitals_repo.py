from sqlalchemy.orm import Session
from app.domain.models import Vitals
from datetime import datetime, timedelta

class VitalsRepository:
    """
    Repository for Vitals entities.
    Handles storage and retrieval of patient vital signs.
    """
    @staticmethod
    def create_vitals(db: Session, data: dict):
        """Create a new vitals record."""
        vitals = Vitals(**data)
        db.add(vitals)
        db.commit()
        db.refresh(vitals)
        return vitals

    @staticmethod
    def get_vitals(db: Session, patient_id=None, encounter_id=None, last_minutes=None):
        """
        Retrieve vitals based on filters.
        Can filter by patient, encounter, or time range.
        """
        query = db.query(Vitals)
        if patient_id:
            query = query.filter(Vitals.patient_id == patient_id)
        if encounter_id:
            query = query.filter(Vitals.encounter_id == encounter_id)
        if last_minutes:
            since = datetime.utcnow() - timedelta(minutes=int(last_minutes))
            query = query.filter(Vitals.timestamp >= since)
            
        return query.order_by(Vitals.timestamp.desc()).all()

    @staticmethod
    def get_latest_vitals(db: Session, encounter_id: int):
        """Get the most recent vitals reading for an encounter."""
        return db.query(Vitals).filter(
            Vitals.encounter_id == encounter_id
        ).order_by(Vitals.timestamp.desc()).first()
