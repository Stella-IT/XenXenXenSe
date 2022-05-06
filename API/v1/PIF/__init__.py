from typing import Optional
from xmlrpc.client import Fault

from fastapi import APIRouter, Depends, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.PIF import PIF
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.PIF.info import router as _pif_info
from API.v1.PIF.list import router as _pif_list
from app.settings import Settings


# === Condition Checker ===
async def verify_pif_uuid(cluster_id: str, pif_uuid: Optional[str] = None):
    if pif_uuid is None:
        return

    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        vif = PIF.get_by_uuid(session, pif_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(
                status_code=404, detail=f"PIF {pif_uuid} does not exist"
            )

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
pif_router = APIRouter(dependencies=[Depends(verify_pif_uuid)])

pif_router.include_router(_pif_list, tags=["pif"])
pif_router.include_router(_pif_info, tags=["pif"])
