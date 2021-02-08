from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VBD import VBD

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

router = APIRouter()


@router.delete("/{cluster_id}/vbd/{vbd_uuid}")
@router.get("/{cluster_id}/vbd/{vbd_uuid}/delete")
async def vbd_delete(cluster_id: str, vbd_uuid: str):
    """ Destroy VBD by UUID """
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vbd: VBD = VBD.get_by_uuid(session=session, uuid=vbd_uuid)

        if vbd is not None:
            ret = dict(success=True, data=vbd.destroy())
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
