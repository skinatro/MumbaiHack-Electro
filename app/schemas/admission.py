from pydantic import BaseModel
from typing import Optional, List

class AdmissionRequest(BaseModel):
    name: str                       # patient full name
    age: int
    gender: Optional[str] = None       # "M", "F", "O", or free-text
    symptoms: List[str]             # e.g. ["chest pain", "shortness of breath"]
    complaint_description: str      # free-text description
    severity_hint: Optional[str] = None  # "low" | "medium" | "high" | None
    preferred_department: Optional[str] = None  # e.g. "ICU", "General"

class AdmissionResponse(BaseModel):
    encounter_id: int
    patient_id: int
    room_id: int
    room_number: str
    department: str
    status: str                      # encounter status
    assigned_doctor_id: Optional[int]   # if assigned, else None
    triage_decision: str             # "ICU", "General", etc.
    notes: str                       # short summary of decision
