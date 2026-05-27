from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class SchemaLoading1c(BaseModel):
    # id: Optional[int]
    phone: Optional[str]
    dogovor: Optional[str]
    dolg: Optional[Decimal]
    pay: Optional[Decimal]
    pre_pay: Optional[int]
    bill_status: Optional[bool]
    date: Optional[str]
    user_loading: Optional[int] 

class SchemaGetPhone(BaseModel):
    phone: Optional[str]