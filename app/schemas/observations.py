from pydantic import BaseModel, Field
from datetime import datetime

class CreateObservationRequest(BaseModel):
    encounter_id: int = Field(..., gt=0)
    note: str = Field(..., min_length=1)

class ObservationResponse(BaseModel):
    id: int
    author_id: int
    note: str
    created_at: datetime

    class Config:
        from_attributes = True
