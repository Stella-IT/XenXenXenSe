from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Interface import NameDescriptionArgs
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/metadata")
@router.get("/{cluster_id}/template/{vm_uuid}/metadata")
async def instance_get_metadata(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Metadata """
    try:
        session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=True, data={
            "name": _vm.get_name(),
            "description": _vm.get_description()
        })

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)


@router.put("/{cluster_id}/vm/{vm_uuid}/metadata")
@router.put("/{cluster_id}/template/{vm_uuid}/metadata")
async def instance_set_description(
    cluster_id: str, vm_uuid: str, args: NameDescriptionArgs
):
    """ Set Instance (VM/Template) Description """
    try:
        session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )

        _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=_vm.set_description(args.description))

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
