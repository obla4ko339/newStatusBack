from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from tortoise.exceptions import DoesNotExist
from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.models.user import User
from src.services.sites import Sites
from pydantic import BaseModel
from src.api.v1.endpoints.auth import get_current_user

router = APIRouter(prefix="/sites", tags=["sites"])

@router.get("/")
async def get_objects(current_user: User = Depends(get_current_user)):
    try:
        sites = Sites()
        data = await sites.getSite()
        return data
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")

class SiteRequest(BaseModel):
    Id: str

@router.post("/info")
async def get_sites_info(request: SiteRequest, current_user: User = Depends(get_current_user)):
    try:
        Id = request.Id 
        sites = Sites()
        data = await sites.getSitesID(Id)
        return data
    except Exception as error:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Произошла ошибка при получении информации: {str(error)}"
        )

class SiteFilter(BaseModel):
    filter: object

@router.post("/sitesfilter")
async def get_sites_filter_search_text(request: SiteFilter, current_user: User = Depends(get_current_user)):
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
            detail=f"Произошла ошибка при получении информации: {str(error)}"
        )

class SiteSet(BaseModel):
    sites: object

@router.post("/sitesset")
async def set_sites(request: SiteSet, current_user: User = Depends(get_current_user)):
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
            detail=f"Произошла ошибка при получении информации: {str(error)}"
        )

@router.get("/{object_id}", response_model=SecurityObject_Pydantic)
async def get_object(object_id: str, current_user: User = Depends(get_current_user)):
    try:
        return await SecurityObject_Pydantic.from_queryset_single(
            SecurityObject.get(id=object_id)
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")
