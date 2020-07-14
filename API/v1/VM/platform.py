from fastapi import APIRouter
from pydantic import BaseModel

from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/platform")
@router.get("/{cluster_id}/template/{vm_uuid}/platform")
async def instance_get_platform(cluster_id: str, vm_uuid: str):
    """ Get Instance (VM/Template) Platform """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": True, "data": vm.get_platform()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret

@router.get("/{cluster_id}/vm/{vm_uuid}/platform/{name}")
@router.get("/{cluster_id}/template/{vm_uuid}/platform/{name}")
async def instance_set_platform_property_byname(cluster_id: str, vm_uuid: str, name: str):
    """ Get Instance (VM/Template) Platform Property by Name """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": True, "data": vm.get_platform()[name]}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/platform/{name}/{var}")
@router.get("/{cluster_id}/template/{vm_uuid}/platform/{name}/{var}")
async def instance_set_platform_property_byname_inurl(cluster_id: str, vm_uuid: str, name: str, var: str):
    """ Set Instance (VM/Template) Platform Property by Name """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    
    if vm is not None:
        data = {}
        data[name] = var
        
        ret = {"success": vm.set_platform(data)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
