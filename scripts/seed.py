from app.core.database import SessionLocal, engine
from app.domain.models import Base, Room, User, Encounter, Patient, Doctor, Vitals, Alert, DischargePlan
from app.repositories.user_repo import UserRepository
from datetime import datetime, timedelta
import random
import json

def seed_data():
    db = SessionLocal()
    
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    # --- Users & Roles ---
    print("Seeding Users...")
    users = [
        ('admin', 'admin123', 'admin'),
        ('dr_house', 'password', 'doctor'),
        ('dr_strangelove', 'password', 'doctor'),
        ('nurse_jackie', 'password', 'nurse'),
        ('patient_zero', 'password', 'patient'),
        ('alice_wonder', 'password', 'patient'),
        ('bob_builder', 'password', 'patient'),
    ]
    
    created_users = {}
    for username, password, role in users:
        user = UserRepository.get_by_username(db, username)
        if not user:
            user = UserRepository.create_user(db, username, password, role)
            print(f"  Created user: {username}")
        created_users[username] = user

    # --- Profiles ---
    print("Seeding Profiles...")
    # Doctors
    if not db.query(Doctor).filter_by(user_id=created_users['dr_house'].id).first():
        UserRepository.create_doctor(db, created_users['dr_house'].id, 'Diagnostics')
    if not db.query(Doctor).filter_by(user_id=created_users['dr_strangelove'].id).first():
        UserRepository.create_doctor(db, created_users['dr_strangelove'].id, 'Surgery')
        
    # Patients
    patients_data = [
        ('patient_zero', '1990-01-01', 'Male'),
        ('alice_wonder', '1985-05-12', 'Female'),
        ('bob_builder', '1978-08-23', 'Male'),
    ]
    
    for username, dob, gender in patients_data:
        user = created_users[username]
        if not db.query(Patient).filter_by(user_id=user.id).first():
            UserRepository.create_patient(db, user.id, dob, gender)
            print(f"  Created patient profile for {username}")

    # --- Rooms ---
    print("Seeding Rooms...")
    if db.query(Room).count() == 0:
        rooms = [
            Room(room_number="101", department="ICU"),
            Room(room_number="102", department="ICU"),
            Room(room_number="201", department="General"),
            Room(room_number="202", department="General"),
        ]
        db.add_all(rooms)
        db.commit()
        print(f"  Created {len(rooms)} rooms")

    # --- Encounters ---
    print("Seeding Encounters...")
    dr_house = db.query(Doctor).filter_by(user_id=created_users['dr_house'].id).first()
    p_zero = db.query(Patient).filter_by(user_id=created_users['patient_zero'].id).first()
    p_alice = db.query(Patient).filter_by(user_id=created_users['alice_wonder'].id).first()
    p_bob = db.query(Patient).filter_by(user_id=created_users['bob_builder'].id).first()
    
    room_101 = db.query(Room).filter_by(room_number="101").first()
    room_201 = db.query(Room).filter_by(room_number="201").first()
    
    # Active Encounter (Patient Zero -> Dr House)
    enc_zero = db.query(Encounter).filter_by(patient_id=p_zero.id, status='active').first()
    if not enc_zero:
        enc_zero = Encounter(
            patient_id=p_zero.id,
            doctor_id=dr_house.id,
            room_id=room_101.id,
            status='active',
            admitted_at=datetime.utcnow() - timedelta(days=2)
        )
        db.add(enc_zero)
        db.commit()
        print("  Created active encounter for Patient Zero")

    # Discharged Encounter (Alice -> Dr House)
    enc_alice = db.query(Encounter).filter_by(patient_id=p_alice.id, status='discharged').first()
    if not enc_alice:
        enc_alice = Encounter(
            patient_id=p_alice.id,
            doctor_id=dr_house.id,
            room_id=room_201.id, # Technically she left, but keeping ref
            status='discharged',
            admitted_at=datetime.utcnow() - timedelta(days=5),
            discharged_at=datetime.utcnow() - timedelta(days=1)
        )
        db.add(enc_alice)
        db.commit()
        print("  Created discharged encounter for Alice")
        
        # Discharge Plan
        plan = DischargePlan(
            encounter_id=enc_alice.id,
            patient_id=p_alice.id,
            summary="Patient recovered fully from mild flu.",
            home_care_instructions="Rest for 2 days. Drink plenty of fluids.",
            recommended_meds=json.dumps([{"name": "Paracetamol", "dose": "500mg", "duration": "3 days"}]),
            followup_days=7
        )
        db.add(plan)
        db.commit()
        print("  Created discharge plan for Alice")

    # --- Vitals & Alerts (for Active Encounter) ---
    print("Seeding Vitals & Alerts...")
    if db.query(Vitals).filter_by(encounter_id=enc_zero.id).count() == 0:
        # Generate 2 hours of vitals
        base_time = datetime.utcnow() - timedelta(hours=2)
        vitals_batch = []
        for i in range(120): # Every minute
            t = base_time + timedelta(minutes=i)
            # Simulate stable but slightly fluctuating
            v = Vitals(
                patient_id=p_zero.id,
                encounter_id=enc_zero.id,
                timestamp=t,
                hr_bpm=random.randint(70, 90),
                spo2_pct=random.randint(96, 100),
                temp_c=round(random.uniform(36.5, 37.2), 1),
                bp_systolic=random.randint(110, 130),
                bp_diastolic=random.randint(70, 85),
                resp_rate_bpm=random.randint(12, 18)
            )
            vitals_batch.append(v)
        db.add_all(vitals_batch)
        db.commit()
        print(f"  Added {len(vitals_batch)} vitals records for Patient Zero")
        
        # Add one resolved alert
        alert = Alert(
            patient_id=p_zero.id,
            encounter_id=enc_zero.id,
            type="tachycardia",
            severity="medium",
            message="HR 110 bpm (Transient)",
            created_at=datetime.utcnow() - timedelta(hours=1),
            resolved=True,
            resolved_at=datetime.utcnow() - timedelta(minutes=50)
        )
        db.add(alert)
        db.commit()
        print("  Added historical alert for Patient Zero")

    print("Seeding complete.")
    db.close()

if __name__ == "__main__":
    seed_data()
