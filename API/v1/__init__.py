from fastapi import APIRouter

from API.v1.Console import console_router
from API.v1.GuestMetrics.info import guest_router
from API.v1.Host import host_router
from API.v1.SR import sr_router
from API.v1.VBD import vbd_router
from API.v1.VDI import vdi_router
from API.v1.VIF import vif_router
from API.v1.VM import vm_router

from app.settings import Settings

from pydantic import BaseModel

router = APIRouter()

_prefix = "/v1"


router.include_router(host_router, prefix=_prefix)
router.include_router(console_router, prefix=_prefix)
router.include_router(sr_router, prefix=_prefix)
router.include_router(vbd_router, prefix=_prefix)
router.include_router(vdi_router, prefix=_prefix)
router.include_router(vif_router, prefix=_prefix)
router.include_router(vm_router, prefix=_prefix)
router.include_router(guest_router, prefix=_prefix)

class XXXS_V1_App(BaseModel):
    version: int
    name: str

class XXXS_V1_Root(BaseModel):
    hello: str
    app: XXXS_V1_App
    clusters: List[str]

@router.get("/", response_model=XXXS_V1_Root)
async def v1_root():
    xen_clusters = Settings.get_xen_clusters()
    xen_cluster_names = [xen_cluster for xen_cluster in xen_clusters ]
    
    return {
        "hello": "world",
        "app": {
            "version": 1,
            "name": "XenXenXenSe"
        },
        "clusters": xen_cluster_names
    }
