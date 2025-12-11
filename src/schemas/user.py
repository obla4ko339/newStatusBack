from pydantic import BaseModel
from datetime import datetime
from typing import Optional




class CreateUser(BaseModel):
    email:str
    group_user:int
    password: str
    tel:str
    username: str
    is_active: bool
    parent:int
