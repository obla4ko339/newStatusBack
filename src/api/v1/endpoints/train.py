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
from src.services.train import Train
from src.crud.bd import getUserRequestToken,checkPermission

router = APIRouter(prefix="/train", tags=["train"])



# Получить список разделов объекта
class TrainIdSites(BaseModel):
    sitesId: str
@router.post("/getTrainSitesId")
async def getTrainSitesId(data:TrainIdSites, request:Request):
    try:
        infoUsers = await getUserRequestToken(request)
        if not infoUsers:
            return False

        # CHECK PERMISSION
        await checkPermission(infoUsers.group_user_id, "sites.view_loop")
        # CHECK PERMISSION

        objTrain = Train()
        zone = await objTrain.getTrainSiteId(data.sitesId)

        return zone
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"{error}"
        )

# Получить список разделов объекта