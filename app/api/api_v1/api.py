from fastapi import APIRouter

from .endpoints.authentication import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.sensors import router as sensors_router
from .endpoints.station import router as station_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(user_router)
# router.include_router(sensors_router)
# router.include_router(station_router)
