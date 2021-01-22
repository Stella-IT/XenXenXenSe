from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter
from fastapi import HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/delete")
@router.delete("/{cluster_id}/vm/{vm_uuid}")
async def vm_delete(cluster_id: str, vm_uuid: str):
    """ Delete VM """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if _vm is not None:
            ret = dict(success=_vm.delete())
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
