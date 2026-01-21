from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist


from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.group_user import crud_get_group_user


router = APIRouter(prefix="/group_user", tags=["group_user"])


@router.get("/get_all_group")
async def get_all_group():
    """
    Получить список всех групп
    """
    try:
        groups = await crud_get_group_user()
        return groups
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")


