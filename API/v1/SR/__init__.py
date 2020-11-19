from fastapi import APIRouter

from API.v1.SR.find import router as _sr_find
from API.v1.SR.info import router as _sr_info
from API.v1.SR.list import router as _sr_list
from API.v1.SR.scan import router as _sr_scan

sr_router = APIRouter()
sr_router.include_router(_sr_list, tags=["sr"])
sr_router.include_router(_sr_find, tags=["sr"])
sr_router.include_router(_sr_info, tags=["sr"])
sr_router.include_router(_sr_scan, tags=["sr"])
