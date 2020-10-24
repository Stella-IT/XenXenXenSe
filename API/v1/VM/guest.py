from fastapi import APIRouter
from XenGarden.session import create_session
from XenGarden.VM import VM

from API.v1.GuestMetrics.serialize import serialize as _guest_serialize
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/guest")
async def vm_guest(cluster_id: str, vm_uuid: str):
    """ Get VM Guest Info """
    session = create_session(
        _id=cluster_id, get_xen_clusters=get_xen_clusters()
    )
    vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if vm is not None:
        ret = dict(success=True, data=_guest_serialize(vm.get_guest_metrics()))
    else:
        session.xenapi.session.logout()
        ret = dict(success=False)

    session.xenapi.session.logout()
    return ret
