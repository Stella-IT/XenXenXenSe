from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from .serialize import serialize

router = APIRouter()


@router.get("/{cluster_id}/vm/list")
async def vm_list(cluster_id: str):
    """ Gets VMs available on Xen Server """

    session = create_session(cluster_id)
    vms = VM.list_vm(session)

    sat = []
    for vm in vms:
        sat.append(serialize(vm))

    ret = {"success": True, "data": sat}
    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/template/list")
async def template_list(cluster_id: str):
    """ Gets Templates available on Xen Server """
    session = create_session(cluster_id)
    vms = VM.list_templates(session)

    sat = []
    for vm in vms:
        sat.append(serialize(vm))

    ret = {"success": True, "data": sat}
    session.xenapi.session.logout()
    return ret
