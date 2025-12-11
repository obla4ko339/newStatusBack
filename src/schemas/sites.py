from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class SitesCreate(BaseModel):
    Id: Optional[str]
    AccountNumber: Optional[int]
    CloudObjectID: Optional[int]
    Name: Optional[str]
    Address: Optional[str]
    Phone1: Optional[str]
    Phone2: Optional[str]
    TypeName: Optional[str]
    EventTemplateName: Optional[str]

class SiteCreate(BaseModel):
    Id: Optional[str]
    AccountNumber: Optional[int]
    CloudObjectID: Optional[int]
    Name: Optional[str]
    Address: Optional[str]
    Phone1: Optional[str]
    Phone2: Optional[str]
    TypeName: Optional[str]
    EventTemplateName: Optional[str]

class SitessCreate(BaseModel):
    sites: List[SiteCreate]


# class SurgardEventRead(SurgardEventCreate):
#     id: int
#     created_at: datetime

#     class Config:
#         orm_mode = True


 