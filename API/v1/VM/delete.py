from fastapi import APIRouter

from XenGarden.VM import VM
from XenGarden.session import create_session

from MySQL.VM import XenVm
from config import get_xen_clusters

router = APIRouter()


@router.get("/{cluster_id}/vm/{vm_uuid}/delete")
@router.delete("/{cluster_id}/vm/{vm_uuid}")
async def vm_delete(cluster_id: str, vm_uuid: str):
    """ Delete VM """
    session = create_session(_id=cluster_id, get_xen_clusters=get_xen_clusters())
    _vm: VM = VM.get_by_uuid(session=session, uuid=vm_uuid)
    if _vm is not None:
        ret = dict(success=_vm.delete())
    else:
        ret = dict(success=False)

    await XenVm().remove_orphaned(cluster_id=cluster_id)

    session.xenapi.session.logout()
    return ret
