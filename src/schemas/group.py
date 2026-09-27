from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, Query




class CreateGroupRole(BaseModel):
    user_group_id:int
    user_group_right_id:int


