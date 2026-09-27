from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.sites import crud_create_sites,crud_get_sites,crud_get_sites_user_id,crud_get_sites_search,crud_get_site_id,crud_update_data

# REDIS
from src.core.redis import redis_container
import json
from pydantic_core import to_jsonable_python 
from fastapi import Response
import time
from fastapi import Request
from src.services.func import generate_numeric_code
from src.services.zones import Zones
from src.crud.bd import getUserRequestToken

router = APIRouter(prefix="/zone", tags=["zone"])



# Получить список разделов объекта
class ZonesIdSites(BaseModel):
    sitesId: str
@router.post("/getZonesSitesId")
async def getZonesSites(data:ZonesIdSites, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers: 
        return False

    objZone = Zones()
    zone = await objZone.getZonesSiteId(data.sitesId)

    return zone
        

# Получить список разделов объекта



# взять раздел под охрану
class ZonesIsArm(BaseModel):
    id: str
@router.post("/isArmZone")
async def isArmZone(data:ZonesIsArm, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return False

    objZone = Zones()
    zone = await objZone.isArmZoneApi(data.id)
    return zone
# взять раздел под охрану


# снять раздел под охрану
class ZonesIsArm(BaseModel):
    id: str
@router.post("/disArmZone")
async def disArmZone(data:ZonesIsArm, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return False

    objZone = Zones()
    zone = await objZone.disArmZoneApi(data.id)
    return zone
# снять раздел под охрану