from fastapi import APIRouter

from API.v1.VBD.delete import router as _vbd_delete
from API.v1.VBD.find_vdi import router as _vbd_find_by_vdi
from API.v1.VBD.info import router as _vbd_info
from API.v1.VBD.list import router as _vbd_list
from API.v1.VBD.media import router as _vbd_media

vbd_router = APIRouter()
vbd_router.include_router(_vbd_list, tags=["vbd"])
vbd_router.include_router(_vbd_info, tags=["vbd"])
vbd_router.include_router(_vbd_find_by_vdi, tags=["vbd"])
vbd_router.include_router(_vbd_media, tags=["vbd"])
vbd_router.include_router(_vbd_delete, tags=["vbd"])
