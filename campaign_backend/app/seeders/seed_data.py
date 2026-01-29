from app.core.database import SessionLocal, Base, engine
from app.models.audience import Audience
from app.models import campaign, audience, analytics

def seed_audiences():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    audiences = [
        Audience(email="user1@example.com", segment="retail"),
        Audience(email="user2@example.com", segment="tech"),
        Audience(email="user3@example.com", segment="retail"),
        Audience(email="user4@example.com", segment="finance"),
        Audience(email="user5@example.com", segment="tech"),
    ]
    
    for aud in audiences:
        if not db.query(Audience).filter_by(email=aud.email).first():
            db.add(aud)
    
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_audiences()
    print("Seed complete")
