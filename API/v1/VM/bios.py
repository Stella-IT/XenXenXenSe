from http.client import RemoteDisconnected
from xmlrpc.client import Fault

import ujson
from fastapi import APIRouter, HTTPException, Request
from XenAPI.XenAPI import Failure
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.Common import xenapi_failure_jsonify
from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/bios")
@router.get("/{cluster_id}/template/{vm_uuid}/bios")
async def instance_get_bios(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) BIOS """
    try:
        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        bios_strings = vm.get_bios_strings()

        session.xenapi.session.logout()
        return dict(success=True, data=bios_strings)
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


@router.put("/{cluster_id}/vm/{vm_uuid}/bios")
@router.put("/{cluster_id}/template/{vm_uuid}/bios")
async def instance_set_bios_property(request: Request, cluster_id: str, vm_uuid: str):
    """ Set Instance (VM/Template) BIOS Property by Name """
    try:
        body = ujson.decode(await request.body())

        session = create_session(
            _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
        )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        ret = dict(success=vm.set_bios_strings(body))

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
