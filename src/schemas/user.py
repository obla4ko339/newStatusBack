from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Query




class CreateUser(BaseModel):
    email:str
    group_user:int
    password: str
    tel:str
    username: str
    is_active: bool
    parent:int
    name_first:Optional[str] = None
    name_last:Optional[str] = None
    name_patronymic:Optional[str] = None
    is_check:Optional[bool] = False




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

class ListUserForPage(BaseModel):
    page:int
    number:int
    search:Optional[str] = None
    filter:Optional[str] = None

class UpdateUser(BaseModel):
    username:str
    password:Optional[str] = None
    email:str
    tel:Optional[str] = None
    id:int


class IsActive(BaseModel):
    id:int
    # is_active:bool