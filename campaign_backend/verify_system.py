from app.core.database import SessionLocal, Base, engine
from app.models.campaign import Campaign, CampaignType, CampaignFrequency, CampaignStatus
from app.models.audience import Audience
from app.models.analytics import CampaignAnalytics
from app.workers.campaign_worker import process_campaign
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_system():
    # Setup
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 1. Check Seeding
        audience_count = db.query(Audience).count()
        logger.info(f"Audience count: {audience_count}")
        if audience_count == 0:
            logger.warning("No audience found. Run seed_data.py first.")
            return

        # 2. Test One-time Campaign for Segment 'tech'
        logger.info("--- Testing One-time Campaign for 'tech' segment ---")
        campaign = Campaign(
            name="Test Tech One-time",
            type=CampaignType.one_time,
            schedule_time=datetime.utcnow(),
            target_segment="tech",
            status=CampaignStatus.pending
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)
        
        analytics = CampaignAnalytics(campaign_id=campaign.id)
        db.add(analytics)
        db.commit()

        # Manually trigger worker
        process_campaign(db, campaign)
        
        db.refresh(campaign)
        db.refresh(analytics)
        
        logger.info(f"Campaign Status: {campaign.status}")
        logger.info(f"Analytics - Sent: {analytics.sent}, Failed: {analytics.failed}")
        # Expect 2 if using the seed data (user2, user5)
        
        # 3. Test Recurring Campaign
        logger.info("--- Testing Recurring Campaign Scheduling ---")
        start_time = datetime.utcnow()
        rec_campaign = Campaign(
            name="Test Weekly News",
            type=CampaignType.recurring,
            schedule_time=start_time,
            target_segment="retail",
            frequency=CampaignFrequency.weekly,
            interval=1,
            status=CampaignStatus.pending
        )
        db.add(rec_campaign)
        db.commit()
        db.refresh(rec_campaign)
        
        rec_analytics = CampaignAnalytics(campaign_id=rec_campaign.id)
        db.add(rec_analytics)
        db.commit()

        process_campaign(db, rec_campaign)
        
        db.refresh(rec_campaign)
        logger.info(f"Recurring Campaign New Schedule: {rec_campaign.schedule_time}")
        logger.info(f"Expected next run: {start_time + timedelta(weeks=1)}")
        
        if abs((rec_campaign.schedule_time - (start_time + timedelta(weeks=1))).total_seconds()) < 60:
            logger.info("Next run schedule calculated correctly.")
        else:
            logger.error("Schedule calculation mismatch!")

    finally:
        db.close()

if __name__ == "__main__":
    verify_system()
