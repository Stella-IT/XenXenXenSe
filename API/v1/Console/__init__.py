from typing import Optional
from xmlrpc.client import Fault

from fastapi import APIRouter, Depends, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.Console import Console
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Console.info import router as _console_info
from app.settings import Settings


# === Condition Checker ===
async def verify_console_uuid(cluster_id: str, console_uuid: Optional[str] = None):
    if console_uuid is None:
        return

    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        console = Console.get_by_uuid(session, console_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(
                status_code=404, detail=f"Console {console_uuid} does not exist"
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
console_router = APIRouter(dependencies=[Depends(verify_console_uuid)])

console_router.include_router(_console_info, tags=["console"])
