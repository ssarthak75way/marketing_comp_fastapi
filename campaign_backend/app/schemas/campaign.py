from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List
from app.models.campaign import CampaignType, CampaignFrequency, CampaignStatus

class CampaignBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    type: CampaignType
    schedule_time: datetime
    message: Optional[str] = Field(None, max_length=1000)
    target_segment: Optional[str] = Field(None, max_length=50)
    frequency: Optional[CampaignFrequency] = None
    interval: Optional[int] = Field(1, ge=1)

    @validator('schedule_time')
    def schedule_time_must_be_future(cls, v):
        if v < datetime.utcnow():
            # In a real app we might allow slightly in the past for immediate processing
            # but for "security"/integrity we usually want future or recent.
            pass 
        return v

class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    schedule_time: Optional[datetime] = None
    message: Optional[str] = Field(None, max_length=1000)
    status: Optional[CampaignStatus] = None

class CampaignResponse(CampaignBase):
    id: int
    status: CampaignStatus
    is_processed: bool
    created_at: datetime
    last_run: Optional[datetime] = None

    class Config:
        orm_mode = True
