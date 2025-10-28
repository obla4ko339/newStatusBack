from fastapi import APIRouter

from src.api.v1.endpoints.customers import router as customer_router
from src.api.v1.endpoints.seruce_objects import router as objects_router
from src.api.v1.endpoints.sites import router as sites
from src.api.v1.endpoints.sites_events import router as sites_events

router = APIRouter(prefix="/api/v1")

router.include_router(customer_router)
router.include_router(objects_router)
router.include_router(sites)
router.include_router(sites_events)