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




class RegUser(BaseModel):
    email:str
    password: str
    confirm: str
    tel:str
    username: str


class CodeEmail(BaseModel):
    email:str


class VerificationData(BaseModel):
    email:str
    code:str