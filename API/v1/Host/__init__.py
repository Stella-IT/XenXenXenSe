from fastapi import APIRouter, HTTPException, Depends
from XenGarden.session import create_session
from app.settings import Settings
from XenAPI.XenAPI import Failure
from API.v1.Common import xenapi_failure_jsonify
from xmlrpc.client import Fault
from typing import Optional

from XenGarden.Host import Host

from API.v1.Host.info import router as _host_info
from API.v1.Host.list import router as _host_list


# === Condition Checker ===
async def verify_host_uuid(cluster_id: str, host_uuid: Optional[str] = None):
    if host_uuid is None:
        return
    
    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        host = Host.get_by_uuid(session, host_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(status_code=404, detail=f"Host {host_uuid} does not exist")
        
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
host_router = APIRouter(dependencies=[Depends(verify_host_uuid)])

host_router.include_router(_host_list, tags=["host"])
host_router.include_router(_host_info, tags=["host"])
