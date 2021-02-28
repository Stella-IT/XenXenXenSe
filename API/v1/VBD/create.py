from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VBD import VBD
from XenGarden.VDI import VDI
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Interface import VBDCreateArgs
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vbd/create")
async def vbd_create(cluster_id: str, create_args: VBDCreateArgs):
    """ Create VBD """
    try:
        session = create_session(
            cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm = VM.get_by_uuid(session, create_args.vm_uuid)
        vdi = VDI.get_by_uuid(session, create_args.vdi_uuid)

        vbd: VBD = VBD.create(
            session,
            vm,
            vdi,
            **create_args.dict(),
        )

        if vbd is not None:
            vbd_uuid = vbd.get_uuid()
            ret = Response(
                "",
                status_code=302,
                headers={"Location": f"/v1/{cluster_id}/vbd/{vbd_uuid}"},
            )
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
