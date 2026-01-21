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