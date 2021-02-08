from fastapi import APIRouter, HTTPException, Depends
from XenGarden.session import create_session
from app.settings import Settings
from XenAPI.XenAPI import Failure
from API.v1.Common import xenapi_failure_jsonify
from xmlrpc.client import Fault
from typing import Optional

from XenGarden.GuestMetrics import GuestMetrics

from API.v1.GuestMetrics.info import router as _guest_info


# === Condition Checker ===
async def verify_guest_uuid(cluster_id: str, guest_uuid: Optional[str] = None):
    if guest_uuid is None:
        return
    
    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        guest_metrics = GuestMetrics.get_by_uuid(session, guest_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(status_code=404, detail=f"GuestMetrics {guest_uuid} does not exist")
        
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
guest_router = APIRouter(dependencies=[Depends(verify_guest_uuid)])

guest_router.include_router(_guest_info, tags=["guest"])
