from app.core.database import SessionLocal, engine, Base
from app.models.audience import Audience
from app.models.campaign import Campaign, CampaignType, CampaignFrequency, CampaignStatus
from app.models.analytics import CampaignAnalytics
from datetime import datetime, timedelta

def seed_data():
    db = SessionLocal()
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Seed Audiences
        if db.query(Audience).count() == 0:
            print("Seeding audiences...")
            audiences = [
                Audience(email="tech_fan1@example.com", segment="tech"),
                Audience(email="tech_fan2@example.com", segment="tech"),
                Audience(email="fashion_ista1@example.com", segment="fashion"),
                Audience(email="fashion_ista2@example.com", segment="fashion"),
                Audience(email="general_user1@example.com", segment="general"),
                Audience(email="general_user2@example.com", segment="general"),
            ]
            db.bulk_save_objects(audiences)
            db.commit()
            print("Audiences seeded.")

        # Seed an initial campaign if none exists
        if db.query(Campaign).count() == 0:
            print("Seeding initial campaigns...")
            # 1. One-time campaign (due now)
            c1 = Campaign(
                name="Welcome Techies",
                type=CampaignType.one_time,
                schedule_time=datetime.utcnow(),
                message="Welcome to our new tech portal!",
                target_segment="tech",
                status=CampaignStatus.pending
            )
            db.add(c1)
            db.commit()
            db.refresh(c1)
            db.add(CampaignAnalytics(campaign_id=c1.id))

            # 2. Recurring campaign (every 10 seconds)
            c2 = Campaign(
                name="Fashion Weekly Update",
                type=CampaignType.recurring,
                schedule_time=datetime.utcnow() + timedelta(seconds=5),
                message="Check out this week's top trends.",
                target_segment="fashion",
                frequency=CampaignFrequency.secondly,
                interval=10,
                status=CampaignStatus.pending
            )
            db.add(c2)
            db.commit()
            db.refresh(c2)
            db.add(CampaignAnalytics(campaign_id=c2.id))
            
            db.commit()
            print("Campaigns seeded.")

    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
