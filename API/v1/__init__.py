from fastapi import APIRouter

from API.v1.Console import console_router
from API.v1.GuestMetrics.info import guest_router
from API.v1.Host import host_router
from API.v1.SR import sr_router
from API.v1.VBD import vbd_router
from API.v1.VDI import vdi_router
from API.v1.VIF import vif_router
from API.v1.VM import vm_router
from API.v1.root import root_router


_prefix = "/v1"
router = APIRouter()

router.include_router(root_router, prefix=_prefix)
router.include_router(host_router, prefix=_prefix)
router.include_router(console_router, prefix=_prefix)
router.include_router(sr_router, prefix=_prefix)
router.include_router(vbd_router, prefix=_prefix)
router.include_router(vdi_router, prefix=_prefix)
router.include_router(vif_router, prefix=_prefix)
router.include_router(vm_router, prefix=_prefix)
router.include_router(guest_router, prefix=_prefix)
