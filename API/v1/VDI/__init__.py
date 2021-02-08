from fastapi import APIRouter, HTTPException, Depends
from XenGarden.session import create_session
from app.settings import Settings
from XenAPI.XenAPI import Failure
from API.v1.Common import xenapi_failure_jsonify
from xmlrpc.client import Fault
from typing import Optional

from XenGarden.VDI import VDI

from API.v1.VDI.delete import router as _vdi_delete
from API.v1.VDI.find import router as _vdi_find
from API.v1.VDI.info import router as _vdi_info
from API.v1.VDI.list import router as _vdi_list

# === Condition Checker ===
async def verify_vdi_uuid(cluster_id: str, vdi_uuid: Optional[str] = None):
    if vdi_uuid is None:
        return
      
    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        vdi = VDI.get_by_uuid(session, vdi_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(status_code=404, detail=f"VDI {vdi_uuid} does not exist")
          
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )

    session.xenapi.session.logout()


# === Router Actions ===
vdi_router = APIRouter(dependencies=[Depends(verify_vdi_uuid)])

vdi_router.include_router(_vdi_list, tags=["vdi"])
vdi_router.include_router(_vdi_find, tags=["vdi"])
vdi_router.include_router(_vdi_info, tags=["vdi"])
vdi_router.include_router(_vdi_delete, tags=["vdi"])
