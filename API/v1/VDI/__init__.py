from fastapi import APIRouter

from API.v1.VDI.delete import router as _vdi_delete
from API.v1.VDI.find import router as _vdi_find
from API.v1.VDI.info import router as _vdi_info
from API.v1.VDI.list import router as _vdi_list

vdi_router = APIRouter()
vdi_router.include_router(_vdi_list, tags=["vdi"])
vdi_router.include_router(_vdi_find, tags=["vdi"])
vdi_router.include_router(_vdi_info, tags=["vdi"])
vdi_router.include_router(_vdi_delete, tags=["vdi"])
