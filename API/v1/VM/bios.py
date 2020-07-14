from fastapi import APIRouter
from pydantic import BaseModel

from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/bios")
@router.get("/{cluster_id}/template/{vm_uuid}/bios")
async def instance_get_bios(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) BIOS """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": True, "data": vm.get_bios_strings()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vm/{vm_uuid}/bios/{name}")
@router.get("/{cluster_id}/template/{vm_uuid}/bios/{name}")
async def instance_set_bios_property_byname(cluster_id: str, vm_uuid: str, name: str):
    """ Get Instance (VM/Template) BIOS Property by Name """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": True, "data": vm.get_bios_strings()[name]}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/bios/{name}/{var}")
@router.get("/{cluster_id}/template/{vm_uuid}/bios/{name}/{var}")
async def instance_set_bios_property_byname_inurl(cluster_id: str, vm_uuid: str, name: str, var: str):
    """ Set Instance (VM/Template) BIOS Property by Name """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        data = {}
        data[name] = var
        
        ret = {"success": vm.set_bios_strings(data)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
