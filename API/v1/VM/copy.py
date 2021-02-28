from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.SR import SR
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Interface import CopyArgs
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vm/{vm_uuid}/copy")
@router.post("/{cluster_id}/template/{vm_uuid}/copy")
async def instance_copy(cluster_id: str, vm_uuid: str, args: CopyArgs):
    """ Copy Instance (VM/Template) """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        _sr: SR = SR.get_by_uuid(session=session, uuid=args.sr_uuid)

        new_vm = await _vm.copy(args.name, _sr)

        if new_vm is not None:
            if args.provision:
                await new_vm.provision()

            new_vm_uuid = new_vm.get_uuid()

            ret = Response(
                "",
                status_code=302,
                headers={"Location": f"/v1/{cluster_id}/vm/{new_vm_uuid}"},
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
