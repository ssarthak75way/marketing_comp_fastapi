from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AnalyticsBase(BaseModel):
    campaign_id: int
    sent: int = 0
    failed: int = 0
    opened: int = 0
    clicked: int = 0

class AnalyticsResponse(AnalyticsBase):
    id: int
    last_updated: datetime

    class Config:
        orm_mode = True
