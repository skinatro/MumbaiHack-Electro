from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VitalsIngestRequest(BaseModel):
    patient_id: int = Field(..., gt=0)
    encounter_id: int = Field(..., gt=0)
    timestamp: datetime
    hr_bpm: Optional[int] = Field(None, ge=0, le=300)
    spo2_pct: Optional[float] = Field(None, ge=0, le=100)
    temp_c: Optional[float] = Field(None, ge=20, le=45)
    bp_systolic: Optional[int] = Field(None, ge=0, le=300)
    bp_diastolic: Optional[int] = Field(None, ge=0, le=300)
    resp_rate: Optional[int] = Field(None, ge=0, le=100)

class VitalsResponse(BaseModel):
    id: int
    timestamp: datetime
    hr_bpm: Optional[int]
    spo2_pct: Optional[float]
    temp_c: Optional[float]

    class Config:
        from_attributes = True
