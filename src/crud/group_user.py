from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from sqlalchemy import desc, distinct, func, or_
from sqlalchemy.orm import Session

from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker
from src.models.surgard_event_sa import SurgardEventSA

from tortoise import Tortoise
from src.core.db import TORTOISE_ORM


from datetime import datetime, timezone

from src.models.user import User
from src.models.sites_user import SitesUser
from src.models.group_user import GroupUser
from src.models.user_group_right import UserGroupRight
from src.models.user_group_role import UserGroupRole
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from src.schemas.sites import SitesCreate
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError
from src.crud.sites_of_user import crud_get_list_all


async def crud_get_group_user():
    try:
        group = await GroupUser.all().values()  
        return group
    except Exception as error:
        return error 


# GET ALL PERMISSIONS
async def crud_get_user_group_right():
    try:
        result = await UserGroupRight.all().values()  
        if not result:
            return {"result":"Данные отсутствуют"}
        return result
    except Exception as error:
        return error 



async def addGroupRight(data):
    if not data:
        return {"result":"3"}
    try:
        newData = data.dict()
        result = await UserGroupRole.create(**newData)
        if result.id:
            return {"result":"ok"}
    except Exception as error:
        print(f'addGroupRight {error}')
        return {"result":f"error {error}"}



async def delGroupRight(data):
    if not data:
        return {"result":"3"}
    try:
        newData = data.dict()
        result = await UserGroupRole.filter(**newData).delete()
        if result > 0:
            return {"result": "deleted"}
        else:
            return {"result": "not_found"}
    except Exception as error:
        print(f'addGroupRight {error}')
        return {"result":f"error {error}"}


async def getGroupRight():

    try:
        result = await UserGroupRole.all().values()
        if result is not None:
            return result
        else:
            return {"result":"no data"}

    except Exception as error:
        print(f'addGroupRight {error}')
        return {"result":f"error {error}"}



