from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.PIF import PIF
from XenGarden.session import create_session

from API.v1.Common import xenapi_failure_jsonify
from API.v1.PIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/pif/{vif_uuid}")
async def pif_get_by_uuid(cluster_id: str, pif_uuid: str):
    """Get PIF by UUID"""
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        pif: PIF = PIF.get_by_uuid(session=session, uuid=pif_uuid)

        if pif is not None:
            ret = dict(success=True, data=await serialize(pif))
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
