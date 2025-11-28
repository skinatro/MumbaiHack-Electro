from app.core.database import SessionLocal, engine
from app.domain.models import Base, Room, User
from app.repositories.user_repo import UserRepository

def seed_data():
    db = SessionLocal()
    
    # Create Tables
    Base.metadata.create_all(bind=engine)
    
    # Create Admin User
    if not UserRepository.get_by_username(db, 'admin'):
        print("Creating admin user...")
        UserRepository.create_user(db, 'admin', 'admin123', 'admin')
        
    # Create Doctor User
    if not UserRepository.get_by_username(db, 'dr_house'):
        print("Creating doctor user...")
        user = UserRepository.create_user(db, 'dr_house', 'password', 'doctor')
        UserRepository.create_doctor(db, user.id, 'Diagnostics')

    # Create Rooms
    if db.query(Room).count() == 0:
        print("Creating rooms...")
        rooms = [
            Room(room_number="101", department="ICU"),
            Room(room_number="102", department="ICU"),
            Room(room_number="201", department="General"),
        ]
        db.add_all(rooms)
        db.commit()

    # Create Patient
    if not UserRepository.get_by_username(db, 'patient_zero'):
        print("Creating patient user...")
        user = UserRepository.create_user(db, 'patient_zero', 'password', 'patient')
        UserRepository.create_patient(db, user.id, '1990-01-01', 'Male')

    # Create Encounter
    from app.domain.models import Encounter, Patient, Doctor
    patient = db.query(Patient).first()
    doctor = db.query(Doctor).first()
    room = db.query(Room).first()
    
    if patient and doctor and room and db.query(Encounter).count() == 0:
        print("Creating encounter...")
        encounter = Encounter(
            patient_id=patient.id,
            doctor_id=doctor.id,
            room_id=room.id,
            status='active'
        )
        db.add(encounter)
        db.commit()
        
    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_data()
