from typing import Optional
from xmlrpc.client import Fault

from fastapi import APIRouter, Depends, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.SR import SR

from API.v1.Common import xenapi_failure_jsonify
from API.v1.SR.find import router as _sr_find
from API.v1.SR.info import router as _sr_info
from API.v1.SR.list import router as _sr_list
from API.v1.SR.scan import router as _sr_scan
from API.v1.SR.vdis import router as _sr_vdis
from app.settings import Settings


# === Condition Checker ===
async def verify_sr_uuid(cluster_id: str, sr_uuid: Optional[str] = None):
    if sr_uuid is None:
        return

    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        sr = SR.get_by_uuid(session, sr_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(status_code=404, detail=f"SR {sr_uuid} does not exist")

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

sr_router = APIRouter(dependencies=[Depends(verify_sr_uuid)])

sr_router.include_router(_sr_list, tags=["sr"])
sr_router.include_router(_sr_find, tags=["sr"])
sr_router.include_router(_sr_info, tags=["sr"])
sr_router.include_router(_sr_scan, tags=["sr"])
