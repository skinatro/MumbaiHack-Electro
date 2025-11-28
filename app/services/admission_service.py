from sqlalchemy.orm import Session
from app.schemas.admission import AdmissionRequest, AdmissionResponse
from app.domain.models import Room, User, Patient, Encounter, Doctor
from app.repositories.user_repo import UserRepository
from datetime import datetime
import random

class AdmissionService:
    @staticmethod
    def decide_department(request: AdmissionRequest) -> str:
        """
        Deterministic triage logic based on symptoms and severity.
        """
        icu_keywords = ["chest pain", "severe", "unconscious", "respiratory distress", "shortness of breath"]
        
        # Check for ICU keywords in symptoms
        for symptom in request.symptoms:
            if any(keyword in symptom.lower() for keyword in icu_keywords):
                return "ICU"
                
        # Check severity hint
        if request.severity_hint == "high":
            return "ICU"
            
        # Check preferred department
        if request.preferred_department:
            # In a real system, we'd check availability here too, but for now we trust the preference 
            # unless it contradicts medical necessity (which we handled above)
            # Actually, the requirement says: "Else if preferred_department is set and a room is available there -> use that."
            # We'll return it here and let allocate_room handle availability check/fallback.
            return request.preferred_department
            
        return "General"

    @staticmethod
    def allocate_room(department: str, db: Session) -> Room:
        """
        Finds the first available room in the specified department.
        Falls back to General if ICU is full, but NOT vice versa (usually).
        Requirement says: "Try 'General' if 'ICU' is full."
        """
        # Try requested department
        room = db.query(Room).filter(
            Room.department == department,
            Room.is_occupied == False
        ).order_by(Room.room_number).first()
        
        if room:
            return room
            
        # Fallback: If ICU full, try General
        if department == "ICU":
            room = db.query(Room).filter(
                Room.department == "General",
                Room.is_occupied == False
            ).order_by(Room.room_number).first()
            if room:
                return room
                
        raise ValueError(f"No rooms available in {department} (or fallback)")

    @staticmethod
    def assign_doctor(db: Session) -> int | None:
        """
        Assigns the first available doctor.
        """
        doctor = db.query(Doctor).first()
        return doctor.id if doctor else None

    @staticmethod
    def auto_admit(request: AdmissionRequest, db: Session) -> AdmissionResponse:
        # 1. Create or reuse User + Patient
        # Simple heuristic: check by name. In production, use DOB/Phone.
        # We'll generate a username from name.
        
        username_base = request.name.lower().replace(" ", "_")
        # Check if user exists (by username for simplicity, or we could search by name if User had name field)
        # User model only has username. Let's assume username = slugified name.
        
        user = UserRepository.get_by_username(db, username_base)
        
        if not user:
            # Create new user
            # Handle duplicate username by appending random suffix if needed? 
            # For hackathon, just append random number if exists? 
            # Or just use the base and fail if exists but not same person?
            # The requirement says: "If user doesn’t exist... Create a User... If a matching user/patient exists, reuse Patient."
            
            # Let's try to find a user that MIGHT be this person. 
            # Since we don't have name in User, we rely on username.
            
            try:
                user = UserRepository.create_user(db, username_base, "changeme", "patient")
                # Create Patient profile
                # We don't have DOB in request? 
                # Request has age. We can approximate DOB.
                approx_dob = datetime(datetime.now().year - request.age, 1, 1)
                patient = UserRepository.create_patient(db, user.id, approx_dob.strftime("%Y-%m-%d"), request.gender or "Unknown")
            except Exception:
                # If creation fails (e.g. username taken), try to fetch again or append suffix
                # For simplicity, let's assume unique names for now or handle gracefully
                # If username exists, we reuse it.
                user = UserRepository.get_by_username(db, username_base)
                patient = user.patient_profile
        else:
            patient = user.patient_profile
            if not patient:
                 # Should not happen if created correctly, but handle it
                 approx_dob = datetime(datetime.now().year - request.age, 1, 1)
                 patient = UserRepository.create_patient(db, user.id, approx_dob.strftime("%Y-%m-%d"), request.gender or "Unknown")

        # 2. Triage
        department = AdmissionService.decide_department(request)
        
        # 3. Allocate Room
        room = AdmissionService.allocate_room(department, db)
        room.is_occupied = True
        db.add(room) # Mark occupied
        
        # 4. Assign Doctor
        doctor_id = AdmissionService.assign_doctor(db)
        
        # 5. Create Encounter
        encounter = Encounter(
            patient_id=patient.id,
            doctor_id=doctor_id,
            room_id=room.id,
            status="active",
            admitted_at=datetime.utcnow()
        )
        db.add(encounter)
        db.commit()
        db.refresh(encounter)
        
        # 6. Return Response
        return AdmissionResponse(
            encounter_id=encounter.id,
            patient_id=patient.id,
            room_id=room.id,
            room_number=room.room_number,
            department=room.department, # Actual room department (could be fallback)
            status=encounter.status,
            assigned_doctor_id=doctor_id,
            triage_decision=department, # The INTENDED department
            notes=f"Admitted to {room.department} (Triage: {department}). Reason: {request.symptoms[0] if request.symptoms else 'Checkup'}"
        )
