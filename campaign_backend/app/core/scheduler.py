from apscheduler.schedulers.background import BackgroundScheduler
from app.core.database import SessionLocal
from app.models.campaign import Campaign, CampaignStatus
from app.workers.campaign_worker import process_campaign
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_and_run_campaigns():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        # Find campaigns that are pending, active, and due
        due_campaigns = db.query(Campaign).filter(
            Campaign.status == CampaignStatus.pending,
            Campaign.is_active == True,
            Campaign.schedule_time <= now
        ).all()

        if not due_campaigns:
            return

        logger.info(f"Found {len(due_campaigns)} due campaigns. Starting processing...")
        
        for campaign in due_campaigns:
            try:
                process_campaign(db, campaign)
                logger.info(f"Successfully processed campaign: {campaign.name}")
            except Exception as e:
                logger.error(f"Failed to process campaign {campaign.name}: {e}")
                campaign.status = CampaignStatus.failed
                db.commit()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Check every 5 seconds for granular scheduling
    scheduler.add_job(check_and_run_campaigns, 'interval', seconds=10)
    scheduler.start()
    logger.info("Scheduler started successfully.")
