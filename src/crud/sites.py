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
from src.schemas.sites import SitesCreate
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError
from src.crud.sites_of_user import crud_get_list_all



# вывести объеты по поиску start
async def crud_get_sites_search(data:object):
    # print(data.search_term)
    try:
        if data:
            user_id = data.user_id
            group = data.group_user
            search_pattern = f"%{data.search_term}%"
            if group == 1:
                sql = f"""
                    SELECT * FROM sites
                    where 
                    sites."Name" like $1 
                    or
                    sites."Address" like $1 
                    or
                    sites."AccountNumber"::text like $1 
                    """
            else:
                sql = f"""
                    SELECT * FROM public.user_object
                    left join sites on object_id=sites."AccountNumber"
                    left join users on user_id=users."id"
                    where users."id" = {user_id} and (
                        sites."Name" like $1 
                        or
                        sites."Address" like $1 
                        or
                        sites."AccountNumber"::text like $1  
                    )
                    """
            # print(sql)
            connection = Tortoise.get_connection("default")
            result = await connection.execute_query_dict(sql,[search_pattern])
            return result
    except Exception as error:
        return error  
# вывести объеты по поиску END


# вывести объеты по определенному ползователю и группе start
async def crud_get_sites_user_id(data:object):
    # print( "group ",data.get("user_id"))
    # print( "user_id ",group) 
    try:
        if data:
            user_id = data.user_id if hasattr(data, 'user_id') else data.get("user_id")
            group = data.group_user if hasattr(data, 'group_user') else data.get("group_user")
            
            if group == 1:
                sql = f"""
                    SELECT * FROM sites
                    
                    """
            else:
                sql = f"""
                    SELECT * FROM public.user_object
                    left join sites on object_id=sites."AccountNumber"
                    left join users on user_id=users."id"
                    where users."id" = $1
                    """
            connection = Tortoise.get_connection("default")
            if group == 1:
                result = await connection.execute_query_dict(sql,[])
            else:
                result = await connection.execute_query_dict(sql,[user_id])
            return result
    except Exception as error:
        return error  
# вывести объеты по определенному ползователю и группе END
    



async def crud_create_sites(data: SitesCreate):
    
    try:
        user_data = data.dict(exclude={''})
        # print(user_data['AccountNumber'])
        search_criteria = {
        'Id': user_data['Id'],
        'AccountNumber': user_data['AccountNumber']
        }
        defaults = {
            k: v for k, v in user_data.items() 
            if k not in ['Id', 'AccountNumber']
        } 
        res = await Sites.get_or_create(
            defaults=defaults,
            **search_criteria
        )
        # print("create sites")
        return "create sites"

    except Exception as error:
        print(error)
        return error   

async def crud_get_sites():
    selectSites = await crud_get_list_all()
    resultIsActive = []
    for obj in selectSites:
        resultIsActive.append(obj.get("site_id"))
    getSites = await Sites.filter(AccountNumber__not_in=resultIsActive).values()
    return getSites

 
async def crud_get_sites_all(userID:int, userGroup:int):
    try:

        data = {"user_id":userID, "group_user":userGroup}
        result = await crud_get_sites_user_id(data)
        # result = await Sites.all().values()  
        return result
    except Exception as error:
        return error



async def crud_get_site_id(AccountNumber:int):
    if AccountNumber:
        result = await Sites.filter(AccountNumber=AccountNumber).first()
        if result is not None:
            return result  

async def crud_update_data(data:object):
    try:
        obj = dict(data)
        result = await Sites.filter(AccountNumber = obj.get("AccountNumber")).update(**obj)
        if result == 1:
            return True
        else:
            return False
    except Exception as error:
        return error
    