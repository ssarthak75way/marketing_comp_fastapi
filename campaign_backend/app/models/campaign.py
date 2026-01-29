import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from app.core.database import Base

class CampaignType(enum.Enum):
    one_time = "one_time"
    recurring = "recurring"

class CampaignFrequency(enum.Enum):
    secondly = "secondly"
    hourly = "hourly"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class CampaignStatus(enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(Enum(CampaignType), nullable=False)
    schedule_time = Column(DateTime, nullable=False)
    message = Column(String, nullable=True)
    
    # Selection and Recurring Logic
    target_segment = Column(String, nullable=True)
    frequency = Column(Enum(CampaignFrequency), nullable=True)
    interval = Column(Integer, default=1)
    last_run = Column(DateTime, nullable=True)
    
    status = Column(Enum(CampaignStatus), default=CampaignStatus.pending)
    is_active = Column(Boolean, default=True)
    is_processed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
