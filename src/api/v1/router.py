from fastapi import APIRouter

from src.api.v1.endpoints.customers import router as customer_router
from src.api.v1.endpoints.seruce_objects import router as objects_router

router = APIRouter(prefix="/api/v1")

router.include_router(customer_router)
router.include_router(objects_router)