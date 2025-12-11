from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.sites_of_user import crud_create_site_of_user,crud_get_list_su,crud_del_su,crud_get_list_all
from src.crud.sites import crud_create_sites,crud_get_sites,crud_get_sites_all
from src.schemas.sites import SiteCreate,SitesCreate,SitessCreate
from fastapi import Request
from src.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/sitesuser", tags=["sitesuser"])






@router.get("/user/getsites")
async def getsites(request:Request):
    
    try:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split("Bearer ")[1]
            user = await get_current_user(token)
            userID = user.id
            userGroup = user.group_user
            # print(userID)
            # print(userGroup)
            # getSites = await crud_get_sites()
            
            getSites = await crud_get_sites_all(userID, userGroup)

            # print("getSites ",getSitess)
            return getSites
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = error
        )



@router.post("/user/update")
async def sites_update(data:List[SitesCreate]):
    try:
        for site in data: 
            # print(site)   
            result = await crud_create_sites(site)
            # results.append(result)
            # result = await crud_create_sites(data)
            # return result
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "error create user"
        )


class sitesUser(BaseModel):
    user_id:int
    object_id:int

@router.post("/user/create")
async def create_sites_user(data:sitesUser):
    print(data)
    try:
        result = await crud_create_site_of_user(data)
        return result
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "error create user"
        )



class SiteUserRequest(BaseModel):
    user_id: int
@router.post("/user/getlist")
async def crud_get_list_id(data:SiteUserRequest):
    try:
        data = await crud_get_list_su(data)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении информации: {str(error)}"
    )
    

class SiteUserRequest(BaseModel):
    id: int
@router.post("/user/del")
async def crud_del_id(data:SiteUserRequest):
    try:
        data = await crud_del_su(data)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении информации: {str(error)}"
    )
    
    
class SiteFilter(BaseModel):
    filter: object
@router.post("/sitesfilter")
async def get_sites_filter_search_text(request:SiteFilter):
    print(request.filter)
    try:
        filter = request.filter 
        sites = Sites()
        data = await sites.getSitesFilter(filter)
        print(data)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Произошла ошибка при получении нформации: {str(error)}"
    )

class SiteSet(BaseModel):
    sites: object
@router.post("/sitesset")
async def set_sites(request:SiteSet):
    print(request.sites)
    try:
        sitesNew = request.sites 
        sites = Sites()
        data = await sites.setSites(sitesNew)
        print(data)
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