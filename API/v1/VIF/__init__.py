from fastapi import APIRouter, HTTPException, Depends
from XenGarden.session import create_session
from app.settings import Settings
from XenAPI.XenAPI import Failure
from API.v1.Common import xenapi_failure_jsonify
from xmlrpc.client import Fault
from typing import Optional

from XenGarden.VIF import VIF

from API.v1.VIF.info import router as _vif_info
from API.v1.VIF.ipv4 import router as _vif_ipv4
from API.v1.VIF.ipv4_allowed import router as _vif_ipv4_allowed
from API.v1.VIF.ipv6 import router as _vif_ipv6
from API.v1.VIF.ipv6_allowed import router as _vif_ipv6_allowed
from API.v1.VIF.list import router as _vif_list
from API.v1.VIF.lock import router as _vif_lock
from API.v1.VIF.qos import router as _vif_qos


# === Condition Checker ===
async def verify_vif_uuid(cluster_id: str, vif_uuid: Optional[str] = None):
    if vif_uuid is None:
        return
    
    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        vif = VIF.get_by_uuid(session, vif_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(status_code=404, detail=f"VIF {vif_uuid} does not exist")
        
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
vif_router = APIRouter(dependencies=[Depends(verify_vif_uuid)])

vif_router.include_router(_vif_list, tags=["vif"])
vif_router.include_router(_vif_info, tags=["vif"])
vif_router.include_router(_vif_ipv4, tags=["vif"])
vif_router.include_router(_vif_ipv4_allowed, tags=["vif"])
vif_router.include_router(_vif_ipv6, tags=["vif"])
vif_router.include_router(_vif_ipv6_allowed, tags=["vif"])
vif_router.include_router(_vif_lock, tags=["vif"])
vif_router.include_router(_vif_qos, tags=["vif"])
