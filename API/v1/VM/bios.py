from http.client import RemoteDisconnected
from xmlrpc.client import Fault

from fastapi import APIRouter
from fastapi import HTTPException
from XenGarden.session import create_session
from XenGarden.VM import VM

from app.settings import Settings

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/bios")
@router.get("/{cluster_id}/template/{vm_uuid}/bios")
async def instance_get_bios(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) BIOS """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if vm is not None:
            ret = dict(success=True, data=vm.get_bios_strings())
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


@router.get("/{cluster_id}/vm/{vm_uuid}/bios/{name}")
@router.get("/{cluster_id}/template/{vm_uuid}/bios/{name}")
async def instance_set_bios_property_byname(cluster_id: str, vm_uuid: str, name: str):
    """ Get Instance (VM/Template) BIOS Property by Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if vm is not None:
            ret = dict(success=True, data=vm.get_bios_strings()[name])
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


@router.get("/{cluster_id}/vm/{vm_uuid}/bios/{name}/{var}")
@router.get("/{cluster_id}/template/{vm_uuid}/bios/{name}/{var}")
async def instance_set_bios_property_byname_inurl(
    cluster_id: str, vm_uuid: str, name: str, var: str
):
    """ Set Instance (VM/Template) BIOS Property by Name """
    try:
        try:
            session = create_session(
                _id=cluster_id, get_xen_clusters=Settings.get_xen_clusters()
            )
        except KeyError as key_error:
            raise HTTPException(
                status_code=400, detail=f"{key_error} is not a valid path"
            )

        vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
        if vm is not None:
            data = {name: var}

            ret = dict(success=vm.set_bios_strings(data))
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
