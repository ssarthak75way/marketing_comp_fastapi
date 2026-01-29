from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.services.retry_service import retry_send
from app.models.audience import Audience
from app.models.analytics import CampaignAnalytics
from app.models.campaign import Campaign, CampaignType, CampaignFrequency, CampaignStatus

def calculate_next_run(current_time, frequency, interval):
    if frequency == CampaignFrequency.secondly:
        return current_time + timedelta(seconds=interval)
    elif frequency == CampaignFrequency.hourly:
        return current_time + timedelta(hours=interval)
    elif frequency == CampaignFrequency.daily:
        return current_time + timedelta(days=interval)
    elif frequency == CampaignFrequency.weekly:
        return current_time + timedelta(weeks=interval)
    elif frequency == CampaignFrequency.monthly:
        # Simple monthly increment (approximate)
        return current_time + timedelta(days=30 * interval)
    return None

def process_campaign(db: Session, campaign: Campaign):
    # Update status to processing
    campaign.status = CampaignStatus.processing
    db.commit()

    # Segmentation logic
    query = db.query(Audience)
    if campaign.target_segment:
        query = query.filter(Audience.segment == campaign.target_segment)
    
    audiences = query.all()
    analytics = db.query(CampaignAnalytics).filter_by(campaign_id=campaign.id).first()

    for idx, user in enumerate(audiences):
        success = retry_send(user.email, campaign.name, campaign.message)
        if success:
            analytics.sent += 1
        else:
            analytics.failed += 1
        
        # Commit every 5 users to show progress without overloading the DB
        if (idx + 1) % 5 == 0:
            db.commit()

    # Update metadata
    campaign.last_run = datetime.utcnow()
    
    if campaign.type == CampaignType.recurring:
        campaign.schedule_time = calculate_next_run(campaign.schedule_time, campaign.frequency, campaign.interval)
        campaign.status = CampaignStatus.pending  # Set back to pending for next run
    else:
        campaign.is_processed = True
        campaign.status = CampaignStatus.completed

    db.commit()
