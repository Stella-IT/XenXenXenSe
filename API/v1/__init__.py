from fastapi import APIRouter

from API.v1.Console import console_router
from API.v1.GuestMetrics.info import guest_router
from API.v1.Host import host_router
from API.v1.root import root_router
from API.v1.SR import sr_router
from API.v1.VBD import vbd_router
from API.v1.VDI import vdi_router
from API.v1.VIF import vif_router
from API.v1.VM import vm_router

v1_router = APIRouter()

v1_router.include_router(root_router)
v1_router.include_router(host_router)
v1_router.include_router(console_router)
v1_router.include_router(sr_router)
v1_router.include_router(vbd_router)
v1_router.include_router(vdi_router)
v1_router.include_router(vif_router)
v1_router.include_router(vm_router)
v1_router.include_router(guest_router)
