from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime as dt  

Base = declarative_base()

class SurgardEventSA(Base):
    __tablename__ = "surgard_events"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(10))
    event_type = Column(String(10))
    event_code = Column(String(10))
    group_code = Column(String(10))
    zone_or_user = Column(String(10))
    datetime = Column(DateTime(timezone=False))  
    raw = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=False), default=dt.utcnow)  