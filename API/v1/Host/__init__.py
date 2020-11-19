from fastapi import APIRouter

from API.v1.Host.info import router as _host_info
from API.v1.Host.list import router as _host_list

host_router = APIRouter()
host_router.include_router(_host_list, tags=["host"])
host_router.include_router(_host_info, tags=["host"])
