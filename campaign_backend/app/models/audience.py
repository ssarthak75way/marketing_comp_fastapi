from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Audience(Base):
    __tablename__ = "audiences"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    segment = Column(String, index=True)
