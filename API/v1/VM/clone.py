from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from API.v1.Interface import CloneArgs
from API.v1.VM.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vm/{vm_uuid}/clone")
@router.post("/{cluster_id}/template/{vm_uuid}/clone")
async def instance_clone(cluster_id: str, vm_uuid: str, args: CloneArgs):
    """ Clone Instance (VM/Template) """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        new_vm = await _vm.clone(args.name)

        if new_vm is not None:
            if args.provision:
                await new_vm.provision()

            ret = dict(success=True, data=await serialize(new_vm))
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
