from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter, HTTPException, Request
from starlette.responses import RedirectResponse
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Console.serialize import serialize as _console_serialize
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/console{url_after:path}")
@router.post("/{cluster_id}/vm/{vm_uuid}/console{url_after:path}")
@router.patch("/{cluster_id}/vm/{vm_uuid}/console{url_after:path}")
@router.put("/{cluster_id}/vm/{vm_uuid}/console{url_after:path}")
@router.delete("/{cluster_id}/vm/{vm_uuid}/console{url_after:path}")
async def vm_console(cluster_id: str, vm_uuid: str, url_after: str = ""):
    """ Get the first console of the VM """

    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        consoles: Console = vm.get_consoles()

        if len(consoles) == 0:
            raise HTTPException(
                status_code=404,
                detail=f"Console doesn't exist on VM {vm_uuid}",
            )

        console: Console = consoles[0]
        console_uuid = console.get_uuid()

        return RedirectResponse(
            url=f"/v1/{cluster_id}/console/{console_uuid}{url_after}"
        )
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)


@router.get("/{cluster_id}/vm/{vm_uuid}/consoles")
async def vm_consoles(cluster_id: str, vm_uuid: str):
    """ Get all consoles are available to the VM """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        consoles = vm.get_consoles()

        __consoleList = []
        for console in consoles:
            __consoleList.append(_console_serialize(console))

        ret = dict(success=True, data=__consoleList)

        session.xenapi.session.logout()
        return ret
    except Fault as xml_rpc_error:
        raise HTTPException(
            status_code=int(xml_rpc_error.faultCode),
            detail=xml_rpc_error.faultString,
        )
    except RemoteDisconnected as rd_error:
        raise HTTPException(status_code=500, detail=rd_error.strerror)
