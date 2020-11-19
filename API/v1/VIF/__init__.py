from fastapi import APIRouter

from API.v1.VIF.info import router as _vif_info
from API.v1.VIF.list import router as _vif_list
from API.v1.VIF.qos import router as _vif_qos

vif_router = APIRouter()
vif_router.include_router(_vif_list, tags=["vif"])
vif_router.include_router(_vif_info, tags=["vif"])
vif_router.include_router(_vif_qos, tags=["vif"])
