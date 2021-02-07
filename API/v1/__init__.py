from fastapi import APIRouter, Depends, HTTPException
from XenGarden.session import create_session

from API.v1.Console import console_router
from API.v1.GuestMetrics.info import guest_router
from API.v1.Host import host_router
from API.v1.root import root_router
from API.v1.SR import sr_router
from API.v1.VBD import vbd_router
from API.v1.VDI import vdi_router
from API.v1.VIF import vif_router
from API.v1.VM import vm_router
from app.settings import Settings

v1_router = APIRouter()
v1_router.include_router(root_router)

# === Condition Checker ===
async def verify_cluster_id(cluster_id: str):
    # KeyError Handling
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        session.xenapi.session.logout()
    except KeyError as key_error:
        raise HTTPException(
            status_code=404, detail=f"{key_error} cluster does not exist"
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )


# === API Functions ===

_api_router = APIRouter(dependencies=[Depends(verify_cluster_id)])

_api_router.include_router(host_router)
_api_router.include_router(console_router)
_api_router.include_router(sr_router)
_api_router.include_router(vbd_router)
_api_router.include_router(vdi_router)
_api_router.include_router(vif_router)
_api_router.include_router(vm_router)
_api_router.include_router(guest_router)

# === Add ===
v1_router.include_router(_api_router)
