from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.SR import SR
from XenGarden.VDI import VDI

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings
from API.v1.Interface import SRCopyArgs

router = APIRouter()


@router.post("/{cluster_id}/vdi/{vdi_uuid}/copy")
async def vdi_copy(cluster_id: str, vdi_uuid: str, args: SRCopyArgs):
    """ Get VDI by UUID """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vdi: VDI = VDI.get_by_uuid(session=session, uuid=vdi_uuid)
        sr: SR = SR.get_by_uuid(session=session, uuid=args.sr_uuid)

        new_vdi: VDI = vdi.copy(sr)

        if new_vdi is not None:
            vdi_uuid = new_vdi

            new_vdi_uuid = new_vdi.get_uuid()

            ret = RedirectResponse(f"/v1/{cluster_id}/vdi/{new_vdi_uuid}")
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
