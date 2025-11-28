from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AdmitPatientRequest(BaseModel):
    patient_id: int = Field(..., gt=0)
    doctor_id: int = Field(..., gt=0)

class EncounterResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    room_id: int
    status: str
    admitted_at: Optional[datetime] = None
    room_number: Optional[str] = None

    class Config:
        from_attributes = True
