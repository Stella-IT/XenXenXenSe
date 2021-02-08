from fastapi import APIRouter

from API.v1.GuestMetrics.info import router as _info_router

guest_router = APIRouter()
guest_router.include_router(_info_router, tags=["guest"])
