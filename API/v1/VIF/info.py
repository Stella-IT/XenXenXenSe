from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VIF import VIF

from API.v1.VIF.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vif/{vif_uuid}")
async def vif_get_by_uuid(cluster_id: str, vif_uuid: str):
    """ Get VIF by UUID """
    try:
        session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )

        vif: VIF = VIF.get_by_uuid(session=session, uuid=vif_uuid)

        if vif is not None:
            ret = dict(success=True, data=serialize(vif))
        else:
            ret = dict(success=False)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
