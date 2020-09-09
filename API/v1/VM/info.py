from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}")
@router.get("/{cluster_id}/template/{vm_uuid}")
async def instance_info(cluster_id: str, vm_uuid: str):
    """ Get an Info of VM or Template """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)

    if vm is not None:
        ret = {"success": True, "data": serialize(vm)}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/platform")
async def vm_get_vCPU_platform(cluster_id: str, vm_uuid: str):
    """ Get vCPU Platform """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": True, "data": vm.get_platform()}
    else:
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
