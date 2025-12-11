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
from src.models.sites import Sites
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel


class sitesUser(BaseModel):
    user_id:int
    object_id:int

async def crud_create_site_of_user(data: sitesUser):
    try:
        print(f"Creating SurgardEvent with data: {data}")
        user_data = data.dict()
        # result = await SitesUser.create(
        #     user_id=data.user_id,
        #     site_id=data.object_id 
        # ) 

        result,created = await SitesUser.get_or_create( 
            user_id=data.user_id,
            site_id=data.object_id 
        )
        if created:
            return f"created"
        else:
            return f"dublicat"
        # print(f"✅ Created SitesUser with ID: {result[0]}")
        
        # return result
    except Exception as error:
        print(error)
        return error   


class SiteUserRequest(BaseModel):
    user_id: int
async def crud_get_list_su(user_id:SiteUserRequest):
    # users = await SitesUser.all()
    try:
        if user_id:
            # result = await SitesUser.filter(user_id=user_id.user_id).all() 
            result = await SitesUser.filter(user_id=user_id.user_id).prefetch_related('site')
            print(result)
            return result

    except Exception as error:
        print(error)
        return error

async def crud_get_list_all():
    result = await SitesUser.all().values()
    return result


class SiteDelRequest(BaseModel):
    id: int
async def crud_del_su(data:SiteDelRequest):
    try:
        if data:
            result = await SitesUser.filter(id=data.id).delete()
            return result
    except Exception as error:
        print(error)
        return error