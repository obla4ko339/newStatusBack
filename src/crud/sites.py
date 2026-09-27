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
from src.models.sites_local_info import SitesLocalInfo
from src.models.customers import Customer
from src.schemas.surgard_event import SurgardEventCreate
from src.schemas.user import CreateUser
from src.schemas.sites import SitesCreate
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from tortoise.exceptions import IntegrityError
from src.crud.sites_of_user import crud_get_list_all

from src.services.sites import Sites as SitesObj



# вывести объеты по поиску start
async def crud_get_sites_search(data:object):
    # print(data.search_term)
    try:
        if data:
            user_id = data['user_id']
            group = data['group_user']

            offset = (data['page'] - 1) * data['number']
            limit = data['number']

            search_pattern = f"%{data['search_term']}%"
            if group == 1:
                sql = f"""
                    SELECT * FROM sites
                    where 
                    sites."Name" like $1 
                    or
                    sites."Address" like $1 
                    or
                    sites."AccountNumber"::text like $1 
                    LIMIT $2 OFFSET $3
                    """
                sql_total = f"""
                    SELECT count(*) as total FROM sites
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
            response_data = {"total": 0, "result": []}
            connection = Tortoise.get_connection("default")
            if group == 1:
                result_data = await connection.execute_query_dict(sql,[search_pattern,limit, offset ])
                result_total = await connection.execute_query_dict(sql_total,[search_pattern])
                response_data['total'] = result_total[0]['total'] if result_total[0]['total'] else 0
                response_data['result'] = result_data
            else:
                result = await connection.execute_query_dict(sql,[search_pattern])
            return response_data
    except Exception as error:
        print(f"crud_get_sites_search {error}")
        return error  
# вывести объеты по поиску END


# вывести объеты по определенному ползователю и группе start
async def crud_get_sites_user_id(data:object):
    # print( "group ",data.get("user_id"))
    # print( "user_id ",group) 
    
    try:
        if data:
            user_id = data.user_id if hasattr(data, 'user_id') else data.get("user_id")
            group = data.group_user_id if hasattr(data, 'group_user') else data.get("group_user")
            search = data.get("search", None) 

            offset = (data['page'] - 1) * data['number']
            limit = data['number']

            if group == 1:
                # result
                sql = f""" SELECT 
                    sites.*, 
                    sites_local_info.local_adress, 
                    sites_local_info.local_name, 
                    sites_local_info.local_tel
                 FROM sites """
                sql += f""" left join sites_local_info on sites."AccountNumber"=sites_local_info."sites_id" """
                if search:
                    sql += f""" where "Name" like $3 """

                sql += f""" LIMIT $1 OFFSET $2 """
                # result
                
                # total
                sql_total = f"""
                    SELECT count(*) as total FROM public.sites
                    """
                if search:
                    sql_total += f""" where "Name" like $1 """
                # total
                
            else:
                # result
                sql = f"""
                    SELECT 
                        sites.*, 
                    sites_local_info.local_adress, 
                    sites_local_info.local_name, 
                    sites_local_info.local_tel
                     FROM public.user_object
                    left join sites on object_id=sites."AccountNumber"
                    left join sites_local_info on sites."AccountNumber"=sites_local_info."sites_id"
                    left join users on user_id=users."id"
                    where user_object."active"=true and
                    """
                if search:
                    sql += f""" "Name" like $4 and """
                sql += f""" users."id" = $1 LIMIT $2 OFFSET $3 """
                # sql += f""" and user_object."active"=true """
                # result

                # total
                sql_total = f"""
                    SELECT count(*) as total FROM public.user_object
                    left join sites on object_id=sites."AccountNumber"
                    left join users on user_id=users."id"
                    where user_object."active"=true and 
                    """
                if search:
                    sql_total += f""" "Name" like $2 and """
                sql_total += f""" users."id" = $1 """
                # total

            connection = Tortoise.get_connection("default")

            print(f' SQL SITS {sql}')
            
            response_data = {"total": 0, "result": []}

            if group == 1:
                if search:
                    search_param = f"%{search}%"
                    result_total = await connection.execute_query_dict(sql_total,[search_param])
                else:
                    result_total = await connection.execute_query_dict(sql_total,[])

                if search:
                    search_param = f"%{search}%"
                    result = await connection.execute_query_dict(sql,[limit, offset, search_param])
                else:
                    result = await connection.execute_query_dict(sql,[limit, offset])
                    
                response_data['total'] = result_total[0]['total'] if result_total[0]['total'] else 0
                response_data['result'] = result
            else:
                if search:
                    search_param = f"%{search}%"
                    result_total = await connection.execute_query_dict(sql_total,[user_id,search_param])
                else:
                    result_total = await connection.execute_query_dict(sql_total,[user_id])

                if search:
                    search_param = f"%{search}%"
                    result = await connection.execute_query_dict(sql,[user_id,limit, offset,search_param])
                else:
                    result = await connection.execute_query_dict(sql,[user_id,limit, offset])

                response_data['total'] = result_total[0]['total'] if result_total[0]['total'] else 0
                response_data['result'] = result
            return response_data
    except Exception as error:
        print(f"crud_get_sites_user_id {error}")
        return error  
# вывести объеты по определенному ползователю и группе END
    


###############################################################
# через таймер идет запрос на получение новых объектов 
# async def cron_create_sites(data:SitesCreate):
#     try:
#         sites = data
#         # print(f"RESULT cron_create_sites--> {sites}")
#         list_sites = []
#         for site in sites:
#             obj = Sites(**site)
#             list_sites.append(obj)

#         if list_sites is not None:
#             await Sites.bulk_create(list_sites, ignore_conflicts=True)
#             print(f"Успешно записано {len(list_sites)} объектов")
    
#     except Exception as error:
#         print(f"ERROR cron_create_sites {error}")
#         return error
###############################################################


###############################################################
# через таймер идет запрос на получение новых объектов 
async def cron_create_sites(data:SitesCreate):
    try:
        sites = data
        list_sites = []
        for site in sites:
            accountNumber = site.get("AccountNumber")
            if not accountNumber:
                continue

            create = await Sites.update_or_create(
                AccountNumber = accountNumber,
                defaults = site
            )
    except Exception as error:
        print(f"ERROR cron_create_sites {error}")
        return error
###############################################################


###############################################################
# через таймер добавляем обновляем ответстенных  
async def cron_create_update_customers():
    try:
        listSites = await Sites.all().values()
        site = SitesObj()
        for item in listSites:
            customers_obj = await site.getCustomersID(item.get('Id'))
            
            if not customers_obj:
                continue

            for custom in customers_obj:
                Id = custom.get('Id')
                if not Id:
                    continue
                custom['sitesId'] = item.get('Id')

                create = await Customer.update_or_create(
                    Id = Id,
                    defaults = custom
                )

            

            


    except Exception as error:
        print(f"ERROR cron_create_update_customers {error}")
        return error
    

###############################################################



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

async def crud_get_site_local_id(AccountNumber:int):

    if AccountNumber:
        result = await SitesLocalInfo.filter(
                        sites_id__AccountNumber=AccountNumber  # Фильтр по полю AccountNumber в Sites
                    ).prefetch_related("sites_id")
        if isinstance(result, list) and len(result) > 0:
            result = result[0]

        if not result:
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
    


async def crud_update_data_local_site(data:object):
    print(data)
    try:
        obj = dict(data)
        
        siteFilter = await SitesLocalInfo.filter(sites_id = obj.get("sites_id")).first()
        
        # result = await SitesLocalInfo.filter(AccountNumber = obj.get("AccountNumber")).update(**obj)
        site = await Sites.filter(AccountNumber=obj.get('sites_id')).first()
        if siteFilter is not None:
            result = await SitesLocalInfo.filter(sites_id = obj.get("sites_id")).update(
                sites_id=site, 
                local_adress=obj.get('Address'), 
                local_tel=obj.get('Phone1'), 
                local_name=obj.get('Name'),
            )
        else:
            # result  = await SitesLocalInfo.create(**obj)
            site = await Sites.filter(AccountNumber=obj.get('sites_id')).first()
            result  = await SitesLocalInfo.create(
                sites_id=site, 
                local_adress=obj.get('Address'), 
                local_tel=obj.get('Phone1'), 
                local_name=obj.get('Name'), 
                )
            
        if result:
            return True
        else:
            return False
    except Exception as error:
        return error



#  активация объекта у пользователя 
async def activeSite(data):
    try:
        id = dict(data)
        result = await SitesUser.filter(id=id.get('id'), active=False).update(active=True)
        return result

    except Exception as error:
        return error