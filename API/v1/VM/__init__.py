from fastapi import APIRouter, HTTPException

from XenGarden.VM import VM

from API.v1.VM.bios import router as _vm_bios
from API.v1.VM.cd import router as _vm_cd
from API.v1.VM.clone import router as _vm_clone
from API.v1.VM.console import router as _vm_console
from API.v1.VM.delete import router as _vm_delete
from API.v1.VM.guest import router as _vm_guest
from API.v1.VM.info import router as _vm_info
from API.v1.VM.list import router as _vm_list
from API.v1.VM.metadata import router as _vm_metadata
from API.v1.VM.platform import router as _vm_platform
from API.v1.VM.power import router as _vm_power
from API.v1.VM.specs import router as _vm_specs
from API.v1.VM.vbd import router as _vm_vbd
from API.v1.VM.vif import router as _vm_vif
from app.settings import Settings
from XenGarden.session import create_session
from xmlrpc.client import Fault

# === Condition Checker ===
async def verify_vm_uuid(cluster_id: str, vm_uuid: str):
    # KeyError Handling
    session = create_session(
        cluster_id, get_xen_clusters=Settings.get_xen_clusters()
    )

    try:
        vm = VM.get_by_uuid(vm_uuid)
        
        if vm is None:
            raise HTTPException(
                status_code=404,
                detail=f"VM {vm_uuid} does not exist"
            )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
        
    session.xenapi.session.logout()


# === Router Checker ===
vm_router = APIRouter()

vm_router.include_router(_vm_bios, tags=["vm"])
vm_router.include_router(_vm_cd, tags=["vm"])
vm_router.include_router(_vm_clone, tags=["vm"])
vm_router.include_router(_vm_delete, tags=["vm"])
vm_router.include_router(_vm_guest, tags=["vm"])
vm_router.include_router(_vm_list, tags=["vm"])
vm_router.include_router(_vm_console, tags=["vm"])
vm_router.include_router(_vm_info, tags=["vm"])
vm_router.include_router(_vm_metadata, tags=["vm"])
vm_router.include_router(_vm_platform, tags=["vm"])
vm_router.include_router(_vm_power, tags=["vm"])
vm_router.include_router(_vm_specs, tags=["vm"])
vm_router.include_router(_vm_vbd, tags=["vm"])
vm_router.include_router(_vm_vif, tags=["vm"])
