from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic

router = APIRouter(prefix="/objects", tags=["objects"])


@router.get("/", response_model=List[SecurityObject_Pydantic])
async def get_objects():
    """
    Получить список всех объектов
    """
    return await SecurityObject_Pydantic.from_queryset(SecurityObject.all())


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