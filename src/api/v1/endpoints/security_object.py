from typing import List
from fastapi import APIRouter, HTTPException
from tortoise.exceptions import DoesNotExist

from src.models.serure_objects import SecurityObject, SecurityObject_Pydantic
from src.services.security_object_section import SecurityObjectSection

router = APIRouter(prefix="/security_object", tags=["security_object"])


@router.post("/arm")
async def handlerSecurity():
    """
    Взять объект под охрану (POST /api/Sites/Arm)
    """
    objectSecurity = SecurityObjectSection()
    result = await objectSecurity.isObjectSecurityArm(id="ea5da272-133f-4350-9188-321c2719449d")
    print(result.text)