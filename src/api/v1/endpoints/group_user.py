from typing import List
from fastapi import APIRouter, HTTPException,status
from tortoise.exceptions import DoesNotExist


from src.services.sites import Sites
from pydantic import BaseModel
from src.crud.group_user import crud_get_group_user,addGroupRight,delGroupRight,getGroupRight,crud_get_user_group_right
from src.crud.bd import getUserRequestToken
from fastapi import Request
from src.schemas.group import CreateGroupRole



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




# get_user_group_right
@router.get("/get_user_group_right")
async def get_user_group_right(request:Request):
    """
    Получить список всех прав
    """
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return {"error":"2"}
    try:
        groups = await crud_get_user_group_right()
        return groups
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")



# распределение груп и ролей запись в БД
@router.post("/add_user_group_role")
async def add_user_group_role(data:CreateGroupRole, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return {"error":"2"}
    try:
        result = await addGroupRight(data)
        return result
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")



# удаление груп и ролей запись в БД
@router.post("/del_user_group_role")
async def del_user_group_role(data:CreateGroupRole, request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return {"error":"2"}
    try:
        result = await delGroupRight(data)
        return result
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")


# получить все распределенные права
@router.get("/get_user_group_role")
async def get_user_group_role(request:Request):
    infoUsers = await getUserRequestToken(request)
    if not infoUsers:
        return {"error":"2"}
    try:
        result = await getGroupRight()
        return result
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Object not found")

