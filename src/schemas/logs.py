from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class SchemaLogs(BaseModel):
    id: Optional[int]
    type: Optional[str]
    desc: Optional[str]
    ip: Optional[str]
    user: Optional[int]
    date_create: Optional[datetime] = None
    section: Optional[str]




class SchemaLogsCreate(BaseModel):
    type: Optional[str]
    desc: Optional[str]
    ip: Optional[str]
    user: Optional[int]
    date_create: Optional[datetime] = None
    section: Optional[str]
