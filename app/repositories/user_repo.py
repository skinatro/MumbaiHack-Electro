from sqlalchemy.orm import Session
from app.domain.models import User, Doctor, Patient
from app.core.security import hash_password

class UserRepository:
    """
    Repository for User, Doctor, and Patient entities.
    Handles database operations for user management.
    """
    @staticmethod
    def get_by_username(db: Session, username: str):
        """Retrieve a user by username."""
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, username, password, role):
        """Create a new user with hashed password."""
        hashed = hash_password(password)
        user = User(username=username, password_hash=hashed, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def create_doctor(db: Session, user_id, specialty):
        """Create a doctor profile for a user."""
        doctor = Doctor(user_id=user_id, specialty=specialty)
        db.add(doctor)
        db.commit()
        return doctor

    @staticmethod
    def create_patient(db: Session, user_id, dob, gender):
        """Create a patient profile for a user."""
        patient = Patient(user_id=user_id, dob=dob, gender=gender)
        db.add(patient)
        db.commit()
        return patient
