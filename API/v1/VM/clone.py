from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Interface import NameArgs
from API.v1.VM.serialize import serialize
from app.settings import Settings

router = APIRouter()


@router.post("/{cluster_id}/vm/{vm_uuid}/clone")
@router.post("/{cluster_id}/template/{vm_uuid}/clone")
async def instance_clone(cluster_id: str, vm_uuid: str, args: NameArgs):
    """ Clone Instance (VM/Template) """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        new_vm = _vm.clone(args.name)
        if new_vm is not None:
            ret = dict(success=True, data=serialize(new_vm))
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
