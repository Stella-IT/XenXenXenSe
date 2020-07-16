from fastapi import APIRouter

from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

router = APIRouter()


@router.get("/{cluster_id}/_vm/list")
async def vm_list(cluster_id: str):
    """ Gets VMs available on Xen Server """

    session = create_session(cluster_id)
    vms = VM.list_vm(session)

    sat = []
    for vm in vms:
        sat.append(vm.serialize())

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
        sat.append(vm.serialize())

    ret = {"success": True, "data": sat}
    session.xenapi.session.logout()
    return ret
