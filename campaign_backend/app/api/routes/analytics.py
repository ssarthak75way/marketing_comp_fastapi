from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.models.analytics import CampaignAnalytics
from app.schemas.analytics import AnalyticsResponse
from app.core.database import SessionLocal

router = APIRouter(prefix="/analytics", tags=["Analytics"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[AnalyticsResponse])
def list_analytics(db: Session = Depends(get_db)):
    return db.query(CampaignAnalytics).all()

@router.get("/{campaign_id}", response_model=AnalyticsResponse)
def get_analytics(campaign_id: int, db: Session = Depends(get_db)):
    analytics = db.query(CampaignAnalytics).filter_by(campaign_id=campaign_id).first()
    return analytics
