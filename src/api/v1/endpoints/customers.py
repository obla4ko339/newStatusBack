from typing import List
from fastapi import APIRouter, Depends, HTTPException
from tortoise.exceptions import DoesNotExist
from src.models.customers import Customer, Customer_Pydantic

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("/", response_model=List[Customer_Pydantic])
async def get_customers():
    """
    Получить список всех клиентов
    """
    return await Customer_Pydantic.from_queryset(Customer.all())


@router.get("/{customer_id}", response_model=Customer_Pydantic)
async def get_customer(customer_id: str):
    """
    Получить клиента по ID
    """
    try:
        return await Customer_Pydantic.from_queryset_single(
            Customer.get(id=customer_id)
        )
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Customer not found")