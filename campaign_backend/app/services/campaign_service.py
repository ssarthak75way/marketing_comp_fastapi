from sqlalchemy.orm import Session
from app.models.campaign import Campaign, CampaignStatus
from app.models.analytics import CampaignAnalytics

def create_campaign(db: Session, campaign_data: dict):
    campaign = Campaign(**campaign_data)
    campaign.status = CampaignStatus.pending
    db.add(campaign)
    db.commit()
    db.refresh(campaign)

    analytics = CampaignAnalytics(campaign_id=campaign.id)
    db.add(analytics)
    db.commit()

    return campaign
