from sqlalchemy.orm import Session
from app.domain.models import Vitals
from datetime import datetime, timedelta

class VitalsRepository:
    @staticmethod
    def create_vitals(db: Session, data: dict):
        vitals = Vitals(**data)
        db.add(vitals)
        db.commit()
        db.refresh(vitals)
        return vitals

    @staticmethod
    def get_vitals(db: Session, patient_id=None, encounter_id=None, last_minutes=None):
        query = db.query(Vitals)
        if patient_id:
            query = query.filter(Vitals.patient_id == patient_id)
        if encounter_id:
            query = query.filter(Vitals.encounter_id == encounter_id)
        if last_minutes:
            since = datetime.utcnow() - timedelta(minutes=int(last_minutes))
            query = query.filter(Vitals.timestamp >= since)
            
        return query.order_by(Vitals.timestamp.desc()).all()
