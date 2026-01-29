from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignResponse
from app.services.campaign_service import create_campaign
from app.workers.campaign_worker import process_campaign
from app.core.database import SessionLocal
from app.models.campaign import Campaign, CampaignStatus

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[CampaignResponse])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).all()

@router.post("/", response_model=CampaignResponse)
def create_campaign_api(
    campaign: CampaignCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    new_campaign = create_campaign(db, campaign.dict())
    return new_campaign

@router.patch("/{campaign_id}/reschedule", response_model=CampaignResponse)
def reschedule_campaign(
    campaign_id: int,
    update: CampaignUpdate,
    db: Session = Depends(get_db)
):
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    campaign.schedule_time = update.schedule_time
    campaign.status = CampaignStatus.pending
    campaign.is_processed = False
    
    db.commit()
    db.refresh(campaign)
    return campaign
