from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from API.v1.VM.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}")
@router.get("/{cluster_id}/template/{vm_uuid}")
async def instance_info(cluster_id: str, vm_uuid: str):
    """ Get an Info of VM or Template """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)

    if vm is not None:
        ret = dict(success=True, data=serialize(vm))
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/vm/{vm_uuid}/platform")
async def vm_get_vCPU_platform(cluster_id: str, vm_uuid: str):
    """ Get vCPU Platform """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        ret = dict(success=True, data=vm.get_platform())
    else:
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret
