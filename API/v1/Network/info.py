from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.Network import Network
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Network.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/network/{network_uuid}")
async def network_get_by_uuid(cluster_id: str, network_uuid: str):
    """Get Virtual Network by UUID"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        network: Network = Network.get_by_uuid(session=session, uuid=network_uuid)

        if network is not None:
            ret = dict(success=True, data=await serialize(network))
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Failure as xenapi_error:
        raise HTTPException(
            status_code=500, detail=xenapi_failure_jsonify(xenapi_error)
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
