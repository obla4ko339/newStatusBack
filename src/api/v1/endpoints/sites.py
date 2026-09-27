from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.sites import crud_create_sites,crud_get_sites,crud_get_sites_user_id,crud_get_sites_search,crud_get_site_id,crud_update_data,crud_update_data_local_site,crud_get_site_local_id

# REDIS
from src.core.redis import redis_container
import json
from pydantic_core import to_jsonable_python 
from fastapi import Response
import time
from fastapi import Request
from src.services.func import generate_numeric_code
from src.crud.bd import getUserRequestToken,checkPermission

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/")
async def get_objects():
    """
    Получить список всех объектов
    """
    try:
        sites = Sites()
        data = await sites.getSite()
        return data
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")




class SiteRequest(BaseModel):
    id: str
@router.post("/info")
async def get_sites_info(request:SiteRequest):
    try:
        Id = request.id 
        sites = Sites()
        data = await sites.getSitesID(Id)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении нформации: {str(error)}"
    )
    


class SiteRequest(BaseModel):
    id: str
@router.post("/customers")
async def get_sites_customers(zone:SiteRequest, request:Request):
    try:
        infoUsers = await getUserRequestToken(request)
        if not infoUsers: 
            return False

        # CHECK PERMISSION
        await checkPermission(infoUsers.group_user_id, "sites.view_responsible")
        # CHECK PERMISSION
        
        Id = zone.id 
        sites = Sites()
        data = await sites.getCustomersID(Id)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении ответственного: {str(error)}"
    )


# вывести объеты по определенному ползователю и группе start
class SiteFilter(BaseModel):
    # user_id: int
    # group_user:int
    page:int
    number:int
@router.post("/getSitesUserId")
async def getSitesUserId(data:SiteFilter, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return False
  
    userInfo = {}
    userInfo["user_id"] = infoUsers.id
    userInfo["group_user"] = infoUsers.group_user_id
    userInfo["page"] = data.page
    userInfo["number"] = data.number

    # REDIS
    start_total = time.perf_counter() 
    cache_key = f"list_sites:user:{userInfo['user_id']}:page:{data.page}:number:{data.number}"
    redis_client = redis_container.client
    # await redis_client.delete("list_sites")
    cache_data_list_sites = await redis_client.get(cache_key)

   

    # Замер только чтения из Redis
    start_redis = time.perf_counter()
    cache_data_list_sites = await redis_client.get(cache_key)
    end_redis = time.perf_counter()

    

    # if cache_data_list_sites:
    #     # return json.loads(cache_data_list_user)
    #     print(f"ВЕРНУЛИ REDIS SITES")
    #     ressponse = Response(content=cache_data_list_sites, media_type="application/json")
    #     return ressponse
    # REDIS

    

    result = await crud_get_sites_user_id(userInfo)
    # print(result)
    # return False
    # REDIS
    json_compatible_data = to_jsonable_python(result)
    # await redis_client.set(cache_key, json.dumps(json_compatible_data), ex=43200 ) # 1 час
    await redis_client.set(cache_key, json.dumps(json_compatible_data), ex=50 ) # 1 час
    # REDIS
    print(f"ВЕРНУЛИ POSTGRES SITES")
    return result
    # try:
    #     # result = 

    # except Exception as error:
    #     return error 
        

# вывести объеты по определенному ползователю и группе end



class SiteSearchUser(BaseModel):
    search_term: str
    page:int
    number:int
@router.post("/sitesfilter")
async def get_sites_filter_search_text(data:SiteSearchUser, request:Request):
    try:    
        infoUsers = await getUserRequestToken(request)
        if not infoUsers:
            return False

        userInfo = {
            "user_id":infoUsers.id,
            "group_user":infoUsers.group_user_id,
            "page":data.page,
            "number":data.number,
            "search_term":data.search_term,
        }


        data = await crud_get_sites_search(userInfo)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении нформации: {str(error)}"
    )






#  Вывести объект по id для редактирования и внесения данных START
class GetSiteId(BaseModel):
    AccountNumber: int
@router.post("/getSiteId")
async def SiteEdit(data:GetSiteId):
    try:
        result = await crud_get_site_id(data.AccountNumber)
        return result
    except Exception as error:
        print(error)
    
    
#  Вывести объект по id для редактирования и внесения данных END


#  Вывести объект по id для редактирования и внесения данных ЛОКАЛЬНЫЙ ВАРИАНТ START
class GetSiteId(BaseModel):
    AccountNumber: int
@router.post("/getSiteIdLocal")
async def SiteEditLocal(data:GetSiteId):
    try:
        result = await crud_get_site_local_id(data.AccountNumber)
        return result
    except Exception as error:
        print(error)
    
    
#  Вывести объект по id для редактирования и внесения данных ЛОКАЛЬНЫЙ ВАРИАНТ END


#  Обновить объекты stast
class UpdateData(BaseModel):
    AccountNumber: int
    Name:str
    Address:str
    Phone1:str
@router.post("/updateData")
async def UpdateData(data:UpdateData):
    try:
        result = await crud_update_data(data)
        return result
    except Exception as error:
        print(error)
#  Обновить объекты end


#  Обновить объекты local stast
class UpdateDataLocalSite(BaseModel):
    sites_id: int
    Name:str
    Address:str
    Phone1:str
@router.post("/updateDataLocalSite")
async def UpdateData(data:UpdateDataLocalSite):
    # print(data)
    try:
        result = await crud_update_data_local_site(data) 
        return result
    except Exception as error:
        print(error)
#  Обновить объекты local end








    
# class SiteFilter(BaseModel):
#     filter: object
# @router.post("/sitesfilter")
# async def get_sites_filter_search_text(request:SiteFilter):
#     print(request.filter)
#     try:
#         filter = request.filter 
#         sites = Sites()
#         data = await sites.getSitesFilter(filter)
#         print(data)
#         return data
#     except Exception as error:
#         raise HTTPException(
#         status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
#         detail=f"Произошла ошибка при получении нформации: {str(error)}"
#     )

class SiteSet(BaseModel):
    sites: object
@router.post("/sitesset")
async def set_sites(request:SiteSet):
    # print(request.sites)
    try:
        sitesNew = request.sites 
        sites = Sites()
        data = await sites.setSites(sitesNew)
        # print(data)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении нформации: {str(error)}"
    )
        


@router.get("/{object_id}", response_model=SecurityObject_Pydantic)
async def get_object(object_id: str):
    """
    Получить объект по ID
    """
    try:
        return await SecurityObject_Pydantic.from_queryset_single(
            SecurityObject.get(id=object_id)
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")




# взять объект под охрану
class SiteIsArm(BaseModel):
    id: str
@router.post("/isArmSite")
async def isArmSite(data:SiteIsArm, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return False

    objSite = Sites()
    zone = await objSite.isArmSiteApi(data.id)
    return zone
# взять объект под охрану


# снять объект с охраны
class SiteDisArm(BaseModel):
    id: str
@router.post("/disArmSite")
async def disArmSite(data:SiteDisArm, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return False

    objSite = Sites()
    zone = await objSite.disArmSiteApi(data.id)
    return zone
# снять объект с охраны