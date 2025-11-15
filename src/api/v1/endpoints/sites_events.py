from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.siteEvents import SiteEvents
from pydantic import BaseModel

router = APIRouter(prefix="/sites_events", tags=["sites_events"])




class SiteRequest(BaseModel):
    Id: str
@router.post("/id")
async def get_sites_events_id(request:SiteRequest):
    try:
        Id = request.Id 
        sites = SiteEvents()
        data = await sites.getSiteEventsId(Id)
        return data
    except Exception as error:
        raise HTTPException(
        status_code = 404,
        detail=f"Произошла ошибка при получении нформации: {str(error)}"
    )
    

class SiteRequestFilter(BaseModel):
    filter: object
    Id: int
@router.post("/params")
async def get_sites_events_params(request:SiteRequestFilter):
    try:
        print(request.filter)
        Id = request.Id 
        sites = SiteEvents()
        # data = await sites.getSiteEventsParams(request.filter, Id)
        data = await sites.getSiteEventsParamsBD(request.filter, Id)
        return data
    except Exception as error:
        raise HTTPException(
            status_code=404,
            detail=f"ОШибка {error}"
        )
