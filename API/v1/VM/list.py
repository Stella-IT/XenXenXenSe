from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from API.v1.VM.serialize import serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/list")
async def vm_list(cluster_id: str):
    """ Gets VMs available on Xen Server """

    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())
    vms = VM.list_vm(session=session)

    __sat = []
    sat = __sat.append
    for vm in vms:
        sat(serialize(vm))

    ret = dict(success=True, data=__sat)
    session.xenapi.session.logout()
    return ret


@router.get("/{cluster_id}/template/list")
async def template_list(cluster_id: str):
    """ Gets Templates available on Xen Server """
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())
    vms = VM.list_templates(session=session)

    __sat = []
    sat = __sat.append
    for vm in vms:
        sat(serialize(vm))

    ret = dict(success=True, data=__sat)
    session.xenapi.session.logout()
    return ret
