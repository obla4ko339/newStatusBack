from src.models.surgard_event import SurgardEvent
from src.schemas.surgard_event import SurgardEventCreate
from sqlalchemy import desc, distinct, func, or_
from sqlalchemy.orm import Session

from datetime import datetime
from src.core.sqlalchemy_engine import async_session_maker
from src.models.surgard_event_sa import SurgardEventSA

from tortoise import Tortoise
from src.core.db import TORTOISE_ORM
from tortoise.expressions import Q


from datetime import datetime, timezone

from src.models.user import User
from src.models.sites_user import SitesUser
from src.models.sites import Sites
from src.models.customers import Customer
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel

from fastapi import HTTPException
from src.services.func import checkPhone, generate_phone_variants, normalize_phone
import re








# получить ответственного по телефону 
async def getCustomersPhone(tel:str):
    if not tel:
        return False

    variants = generate_phone_variants(tel)

    conditions = Q()
    for variant in variants:
        conditions |= Q(
            ObjCustPhone1=variant
        ) | Q(
            ObjCustPhone2=variant
        ) | Q(
            ObjCustPhone3=variant 
        ) | Q(
            ObjCustPhone4=variant
        ) | Q(
            ObjCustPhone5=variant
        )

    customers = await Customer.filter(conditions).all().values()
    return customers if customers else False


    # customer = await Customer.filter(Q( ObjCustPhone1=tel, 
    #                                 ObjCustPhone2=tel, 
    #                                 ObjCustPhone3=tel,
    #                                 ObjCustPhone4=tel,
    #                                 ObjCustPhone5=tel,
    #                                 join_type="OR"
    #                                  )).all().values()
    # if not customer:
    #     return False

    # return customer 



# async def getSitesCustomers(data:List[Dict[Any,Any]]):
async def getSitesCustomers(tel:str):
    customer = await getCustomersPhone(tel)
    if not customer:
        return False
    sitesId = []
    for item in customer:
        sitesId.append(item.get('sitesId'))

    if not sitesId:
        return False

    sites = await Sites.filter(Id__in = sitesId).all().values()

    if not sites:
        return False

    number = []
    for item in sites:
        number.append(item.get('AccountNumber'))

    if number:
        return number


    
    




    