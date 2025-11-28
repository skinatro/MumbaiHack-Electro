from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PatientBasicInfo(BaseModel):
    id: int
    name: str # Assuming we have name, or we'll use username/id
    age: Optional[int] = None
    gender: Optional[str] = None

class RoomInfo(BaseModel):
    id: int
    room_number: str

class ActiveEncounter(BaseModel):
    id: int
    patient: PatientBasicInfo
    room: RoomInfo
    admitted_at: datetime
    status: str

class DoctorPatientListResponse(BaseModel):
    encounters: List[ActiveEncounter]

class VitalsPoint(BaseModel):
    timestamp: datetime
    hr_bpm: Optional[int]
    spo2_pct: Optional[float]
    temp_c: Optional[float]
    bp_systolic: Optional[int]
    bp_diastolic: Optional[int]
    resp_rate: Optional[int]

class ObservationInfo(BaseModel):
    id: int
    note: str
    created_at: datetime
    author_id: int

class EncounterOverviewResponse(BaseModel):
    encounter_id: int
    patient_id: int
    latest_vitals: Optional[VitalsPoint]
    last_observation: Optional[ObservationInfo]
    alerts_count: int
    status: str

class PatientEncounterResponse(BaseModel):
    encounter: Optional[ActiveEncounter]

class PatientVitalsResponse(BaseModel):
    vitals: List[VitalsPoint]
