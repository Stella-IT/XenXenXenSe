from fastapi import APIRouter

from API.v1.VIF.info import router as _vif_info
from API.v1.VIF.list import router as _vif_list
from API.v1.VIF.ipv4 import router as _vif_ipv4
from API.v1.VIF.ipv4_allowed import router as _vif_ipv4_allowed
from API.v1.VIF.ipv6 import router as _vif_ipv6
from API.v1.VIF.ipv6_allowed import router as _vif_ipv6_allowed
from API.v1.VIF.lock import router as _vif_lock
from API.v1.VIF.qos import router as _vif_qos

vif_router = APIRouter()
vif_router.include_router(_vif_info, tags=["vif"])
vif_router.include_router(_vif_list, tags=["vif"])
vif_router.include_router(_vif_ipv4, tags=["vif"])
vif_router.include_router(_vif_ipv4_allowed, tags=["vif"])
vif_router.include_router(_vif_ipv6, tags=["vif"])
vif_router.include_router(_vif_ipv6_allowed, tags=["vif"])
vif_router.include_router(_vif_lock, tags=["vif"])
vif_router.include_router(_vif_qos, tags=["vif"])
