from fastapi import APIRouter

from src.api.v1.endpoints.customers import router as customer_router
from src.api.v1.endpoints.seruce_objects import router as objects_router
from src.api.v1.endpoints.sites import router as sites
from src.api.v1.endpoints.surguard import router as surguard
from src.api.v1.endpoints.sites_events import router as sites_events
from src.api.v1.endpoints.auth import router as auth_router
from src.api.v1.endpoints.sites_of_user import router as sites_user_router
from src.api.v1.endpoints.group_user import router as group_user_router

router = APIRouter(prefix="/api/v1")

router.include_router(customer_router)
router.include_router(objects_router)
router.include_router(sites)
router.include_router(surguard)
router.include_router(sites_events)
router.include_router(auth_router)
router.include_router(sites_user_router)
router.include_router(group_user_router)
