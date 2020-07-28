from fastapi import APIRouter

from XenXenXenSe.VM import VM
from XenXenXenSe.session import create_session

from ..GuestMetrics.serialize import serialize as _guest_serialize

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/guest")
async def vm_guest(cluster_id: str, vm_uuid: str):
    """ Get VM Guest Info """
    session = create_session(cluster_id)
    vm: VM = VM.get_by_uuid(session, vm_uuid)
    if vm is not None:
        ret = {"success": True, "data": _guest_serialize(vm.get_guest_metrics())}
    else:
        session.xenapi.session.logout()
        ret = {"success": False}

    session.xenapi.session.logout()
    return ret
