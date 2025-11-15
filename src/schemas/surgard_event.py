from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SurgardEventCreate(BaseModel):
    account_number: Optional[str]
    event_type: Optional[str]
    event_code: Optional[str]
    group_code: Optional[str]
    zone_or_user: Optional[str]
    datetime: Optional[datetime]
    raw: str


class SurgardEventRead(SurgardEventCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True