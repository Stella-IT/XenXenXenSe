from typing import Optional
from xmlrpc.client import Fault

from fastapi import APIRouter, Depends, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.Network import Network
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Network.info import router as _network_info
from API.v1.Network.list import router as _network_list
from app.settings import Settings


# === Condition Checker ===
async def verify_network_uuid(cluster_id: str, network_uuid: Optional[str] = None):
    if network_uuid is None:
        return

    session = create_session(cluster_id, get_xen_clusters=Settings.get_xen_clusters())

    try:
        network = Network.get_by_uuid(session, network_uuid)

    except Failure as xenapi_error:
        if xenapi_error.details[0] == "UUID_INVALID":
            raise HTTPException(
                status_code=404, detail=f"Network {network_uuid} does not exist"
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
network_router = APIRouter(dependencies=[Depends(verify_network_uuid)])

network_router.include_router(_network_list, tags=["network"])
network_router.include_router(_network_info, tags=["network"])
