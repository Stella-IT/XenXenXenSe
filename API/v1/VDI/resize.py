from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VDI import VDI

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Interface import SizeArgs
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vdi/{vdi_uuid}/resize")
async def vdi_resize(cluster_id: str, vdi_uuid: str, args: SizeArgs):
    """ Resize VDI """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)

        await vdi.resize(args.size)
        ret = dict(success=True)

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
