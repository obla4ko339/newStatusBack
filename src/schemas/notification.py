from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from datetime import datetime



class CreateMessage(BaseModel):
    create_at: Optional[datetime] = None
    message:str
    user_id_from:int
    type:int
    user_id_to: list
    status: bool


class DataMessageApi(BaseModel):
    message:str
    type:int
    user_id_to: list

class IsReadMessageApi(BaseModel):
    id: list[str]


class IsReadMessageApiId(BaseModel):
    id: int



