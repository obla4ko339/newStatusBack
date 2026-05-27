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
from src.models.loading import Loading1c
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from src.schemas.sites import SitesCreate
from src.schemas.loading import SchemaLoading1c,SchemaGetPhone
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError
from src.crud.sites_of_user import crud_get_list_all
from tortoise.exceptions import MultipleObjectsReturned
from typing import List
from src.services.func import checkPhone 


        




async def loading_file_streem1c(data: List[SchemaLoading1c]):
    # print(data)
    for row in data:
        try:
            search_phone = checkPhone(row.pop('phone'))
            search_dogovor = row.pop('dogovor')
            if search_phone == '' or search_phone is None:
                continue
            if search_dogovor == '' or search_dogovor is None:
                continue
        except Exception as error:
            print(row)
            print(error)
        try:
            print(row)
            result = await Loading1c.update_or_create(
            phone=search_phone,
            dogovor=search_dogovor,
            defaults=row)
        except MultipleObjectsReturned:
            print(f"Пропуск: найдено несколько записей для {search_phone} с договором {search_dogovor} ")
            # Loading1c.filter(phone=search_phone, dogovor=search_dogovor).delete()
            continue



async def loading_file(data:SchemaLoading1c):
    # print(data)
    file = data
    # print(file)
    # return False
    for row in file:
        try:
            item = SchemaLoading1c(**row)
        
            data_map = item.model_dump()
            


            search_phone = data_map.pop('phone')
            # if search_phone == "79085810532":
            #     print(item  )
            #     print(data_map  )
            search_dogovor = data_map.pop('dogovor')
            # search_pay = data_map.pop('pay')
        except Exception as error:
            print(row)
            print(error)

        try:
            await Loading1c.update_or_create(
            phone=search_phone,
            dogovor=search_dogovor,
            defaults=data_map)
        except MultipleObjectsReturned:
            print(f"Пропуск: найдено несколько записей для {search_phone} с договором {search_dogovor} ")
            # Loading1c.filter(phone=search_phone, dogovor=search_dogovor).delete()
            continue


    # Loading1c.get_or_create(**file)
    # for row in file:
    #     print(row)

    # try:
    #     group = await GroupUser.get_or_create()  
    #     return group
    # except Exception as error:
    #     return error 


async def get_pay_phone(data:SchemaGetPhone):
    if not data:
        return False 

    data = checkPhone(data)
    try:
        if data:
            result = await Loading1c.get(phone=data).all()
            if result is not None:
                return result
            else:
                return {"error":"Данные отсутствуют"}

    except Exception as error:
        return {"error":"Данные отсутствуют"}