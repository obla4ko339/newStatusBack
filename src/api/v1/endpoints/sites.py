from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.sites import crud_create_sites,crud_get_sites,crud_get_sites_user_id,crud_get_sites_search,crud_get_site_id,crud_update_data

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
    


# вывести объеты по определенному ползователю и группе start
class SiteFilter(BaseModel):
    user_id: int
    group_user:int
@router.post("/getSitesUserId")
async def getSitesUserId(data:SiteFilter):
    result = await crud_get_sites_user_id(data)
    return result
    # try:
    #     # result = 

    # except Exception as error:
    #     return error 
        

# вывести объеты по определенному ползователю и группе end




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







class SiteSearchUser(BaseModel):
    search_term: str
    user_id: int
    group_user:int
@router.post("/sitesfilter")
async def get_sites_filter_search_text(data:SiteSearchUser):
    try:
        data = await crud_get_sites_search(data)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении нформации: {str(error)}"
    )
    
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