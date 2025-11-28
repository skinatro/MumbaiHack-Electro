from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    patient_profile = relationship("Patient", back_populates="user", uselist=False)

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    specialty = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="doctor_profile")
    encounters = relationship("Encounter", back_populates="doctor")

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    dob = Column(DateTime)
    gender = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="patient_profile")
    encounters = relationship("Encounter", back_populates="patient")
    vitals = relationship("Vitals", back_populates="patient")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True)
    department = Column(String)
    is_occupied = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    encounters = relationship("Encounter", back_populates="room")

class Encounter(Base):
    __tablename__ = "encounters"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    status = Column(String) # active, discharged
    auto_discharge_blocked = Column(Boolean, default=False)
    admitted_at = Column(DateTime(timezone=True), server_default=func.now())
    discharged_at = Column(DateTime(timezone=True), nullable=True)
    
    patient = relationship("Patient", back_populates="encounters")
    doctor = relationship("Doctor", back_populates="encounters")
    room = relationship("Room", back_populates="encounters")
    vitals = relationship("Vitals", back_populates="encounter")
    observations = relationship("Observation", back_populates="encounter")
    discharge_plan = relationship("DischargePlan", back_populates="encounter", uselist=False)

class Vitals(Base):
    __tablename__ = "vitals"
    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime(timezone=True))
    hr_bpm = Column(Integer)
    spo2_pct = Column(Integer)
    resp_rate_bpm = Column(Integer)
    bp_systolic = Column(Integer)
    bp_diastolic = Column(Integer)
    temp_c = Column(Float)
    device_flags = Column(ARRAY(String))
    
    encounter = relationship("Encounter", back_populates="vitals")
    patient = relationship("Patient", back_populates="vitals")

class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    author_id = Column(Integer, ForeignKey("users.id"))
    note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    encounter = relationship("Encounter", back_populates="observations")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    timestamp = Column(DateTime(timezone=True)) # This is the time of the event (vitals)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # This is when alert was created
    type = Column(String) # tachycardia, hypoxia, hypertension, fever
    severity = Column(String) # high, medium, low
    message = Column(String)
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    
    patient = relationship("Patient")
    encounter = relationship("Encounter")

class DischargePlan(Base):
    __tablename__ = "discharge_plans"
    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"), unique=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    summary = Column(Text)
    home_care_instructions = Column(Text) # Storing as JSON string or Text
    recommended_meds = Column(Text) # Storing as JSON string or Text
    followup_days = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    generated_by = Column(String) # e.g. "llm"
    
    encounter = relationship("Encounter", back_populates="discharge_plan")
    patient = relationship("Patient")

class FollowupAppointment(Base):
    __tablename__ = "followup_appointments"
    id = Column(Integer, primary_key=True, index=True)
    encounter_id = Column(Integer, ForeignKey("encounters.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    scheduled_for = Column(DateTime(timezone=True))
    status = Column(String, default="pending") # pending, completed, cancelled
    
    encounter = relationship("Encounter")
    patient = relationship("Patient")

class AlertExplanation(Base):
    __tablename__ = "alert_explanations"
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"), unique=True)
    summary = Column(Text)
    risk_level = Column(String) # e.g. "High", "Moderate", "Low"
    suggested_checks = Column(Text) # Storing as JSON string
    suggested_actions = Column(Text) # Storing as JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    alert = relationship("Alert", back_populates="explanation")

# Add relationship to Alert model
Alert.explanation = relationship("AlertExplanation", back_populates="alert", uselist=False)
